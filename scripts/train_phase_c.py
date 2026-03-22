"""Phase C: 노동위 판정례 인용/기각 예측 모델 학습 스크립트

재현 가능한 학습 파이프라인.
시드 고정, 결과 저장, 모델 pkl 출력.

Usage:
    python scripts/train_phase_c.py
    python scripts/train_phase_c.py --output-dir models/phase_c
"""
import sys
import os
import json
import argparse
import pickle
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
from scipy.sparse import hstack, csr_matrix

SEED = 42
SOURCE_JSON = r"C:\Users\iceam\OneDrive\5.산업안전\문서\Obsidian Vault\레퍼런스\최영우\법제처_노동위결정문_전문.json"
MERGED_JSONL = r"retagging/output/merged/merged_42k_v1.jsonl"

# 라벨 판정 패턴
GRANTED_PATTERNS = ['부당하다', '양정이 과하', '합리적 이유가 없', '부당한', '위반에 해당', '부당하므로']
DISMISSED_PATTERNS = ['정당하다', '하자가 없', '존재하지 않', '적격이 없', '볼 수 없', '이유 없다']


def load_data():
    """원본 JSON + merged 태깅 로드"""
    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        src = json.load(f)

    tagged = {}
    with open(MERGED_JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            tagged[d.get('case_id', '')] = d

    return src, tagged


def label_case(result, holding_text):
    """판정결과 + holding_points로 이진 라벨 생성"""
    if result in ('전부인정', '일부인정', '인용', '일부시정', '전부시정'):
        return 1
    if result in ('기각', '각하'):
        return 0
    if result in ('초심유지', '초심취소', '초심일부취소'):
        hp = holding_text[-300:]
        is_granted = any(p in hp for p in GRANTED_PATTERNS)
        is_dismissed = any(p in hp for p in DISMISSED_PATTERNS)
        if is_granted and is_dismissed:
            last_g = max((hp.rfind(p) for p in GRANTED_PATTERNS if p in hp), default=-1)
            last_d = max((hp.rfind(p) for p in DISMISSED_PATTERNS if p in hp), default=-1)
            return 1 if last_g > last_d else 0
        if is_granted:
            return 1
        if is_dismissed:
            return 0
    return None


def build_dataset(src, tagged):
    """학습 데이터셋 구성"""
    records = []
    for key, entry in src.items():
        result = entry.get('판정결과', '')
        tag = tagged.get(key, {})
        primary = tag.get('issue_type_primary', '')

        if not primary:
            continue
        # 노조 사건 제외
        if primary == 'union_activity':
            continue

        hp_text = str(entry.get('판정요지', ''))
        label = label_case(result, hp_text)
        if label is None:
            continue

        records.append({
            'case_id': key,
            'primary': primary,
            'stage': tag.get('employment_stage', 'unknown') or 'unknown',
            'disp_count': len(tag.get('disposition_type', [])),
            'excl_count': len(tag.get('exclusion_flags', [])),
            'sec_count': len(tag.get('issue_type_secondary', [])),
            'hp_text': hp_text,
            'label': label,
        })

    return records


def build_features(records):
    """피처 벡터 생성"""
    pe = LabelEncoder()
    se = LabelEncoder()

    struct = np.column_stack([
        pe.fit_transform([r['primary'] for r in records]),
        se.fit_transform([r['stage'] for r in records]),
        [r['disp_count'] for r in records],
        [r['excl_count'] for r in records],
        [r['sec_count'] for r in records],
    ])

    tfidf = TfidfVectorizer(max_features=500, analyzer='char_wb', ngram_range=(2, 4))
    text_feat = tfidf.fit_transform([r['hp_text'] for r in records])

    X = hstack([csr_matrix(struct), text_feat])
    y = np.array([r['label'] for r in records])

    return X, y, pe, se, tfidf


def train_and_evaluate(X, y, output_dir):
    """모델 학습 + 평가 + 저장"""
    n_granted = int(y.sum())
    n_dismissed = len(y) - n_granted

    print(f"학습 데이터: {len(y)}건")
    print(f"인용: {n_granted} ({n_granted * 100 // len(y)}%)")
    print(f"기각: {n_dismissed} ({n_dismissed * 100 // len(y)}%)")
    print(f"피처: {X.shape[1]}차원")
    print()

    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)

    # 모델 정의
    rf = RandomForestClassifier(
        n_estimators=200, class_weight='balanced',
        random_state=SEED, n_jobs=-1
    )
    xgb = XGBClassifier(
        n_estimators=200, scale_pos_weight=n_dismissed / max(n_granted, 1),
        random_state=SEED, eval_metric='logloss', verbosity=0
    )
    gb = GradientBoostingClassifier(
        n_estimators=100, random_state=SEED
    )

    # Cross-validation
    for name, model in [('RF', rf), ('XGB', xgb), ('GB', gb)]:
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        print(f"{name} 5-fold: {scores.mean():.4f} (+/- {scores.std():.4f})")

    # Train/Test split
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )

    rf.fit(X_tr, y_tr)
    xgb.fit(X_tr, y_tr)
    gb.fit(X_tr.toarray(), y_tr)

    # 앙상블
    rf_proba = rf.predict_proba(X_te)
    xgb_proba = xgb.predict_proba(X_te)
    gb_proba = gb.predict_proba(X_te.toarray())
    ensemble_proba = (rf_proba + xgb_proba + gb_proba) / 3
    ensemble_pred = (ensemble_proba[:, 1] >= 0.5).astype(int)

    print("\n=== XGB 단독 ===")
    print(classification_report(y_te, xgb.predict(X_te), target_names=['기각', '인용']))

    print("=== 앙상블 (RF+XGB+GB 소프트보팅) ===")
    print(classification_report(y_te, ensemble_pred, target_names=['기각', '인용']))

    xgb_pred = xgb.predict(X_te)
    xgb_acc = float(accuracy_score(y_te, xgb_pred))
    ensemble_acc = float(accuracy_score(y_te, ensemble_pred))

    results = {
        'date': datetime.now().isoformat(),
        'seed': SEED,
        'total_samples': len(y),
        'n_granted': n_granted,
        'n_dismissed': n_dismissed,
        'n_features': X.shape[1],
        'xgb_test_accuracy': xgb_acc,
        'ensemble_test_accuracy': ensemble_acc,
        'xgb_report': classification_report(y_te, xgb_pred, target_names=['기각', '인용'], output_dict=True),
        'ensemble_report': classification_report(y_te, ensemble_pred, target_names=['기각', '인용'], output_dict=True),
    }

    # 저장
    os.makedirs(output_dir, exist_ok=True)

    # 모델 pkl
    with open(os.path.join(output_dir, 'xgb_model.pkl'), 'wb') as f:
        pickle.dump(xgb, f)
    with open(os.path.join(output_dir, 'rf_model.pkl'), 'wb') as f:
        pickle.dump(rf, f)
    with open(os.path.join(output_dir, 'gb_model.pkl'), 'wb') as f:
        pickle.dump(gb, f)

    # metrics report JSON
    with open(os.path.join(output_dir, 'metrics_report.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # metrics report MD
    with open(os.path.join(output_dir, 'metrics_report.md'), 'w', encoding='utf-8') as f:
        f.write("# Phase C Metrics Report\n\n")
        f.write(f"- Date: {results['date']}\n")
        f.write(f"- Seed: {SEED}\n")
        f.write(f"- Samples: {results['total_samples']} (인용 {n_granted} / 기각 {n_dismissed})\n")
        f.write(f"- Features: {results['n_features']}\n\n")
        f.write("## Accuracy\n\n")
        f.write(f"| Model | Test Accuracy |\n|-------|:---:|\n")
        f.write(f"| XGB | **{xgb_acc:.4f}** |\n")
        f.write(f"| Ensemble | {ensemble_acc:.4f} |\n\n")
        f.write("## XGB Classification Report\n\n")
        f.write(classification_report(y_te, xgb_pred, target_names=['기각', '인용']))
        f.write("\n## Ensemble Classification Report\n\n")
        f.write(classification_report(y_te, ensemble_pred, target_names=['기각', '인용']))

    # test predictions CSV
    import csv
    csv_path = os.path.join(output_dir, 'test_predictions.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'actual', 'xgb_pred', 'xgb_prob_dismissed', 'xgb_prob_granted',
                         'ensemble_pred', 'ensemble_prob_dismissed', 'ensemble_prob_granted'])
        for i in range(len(y_te)):
            writer.writerow([
                i, int(y_te[i]), int(xgb_pred[i]),
                f"{xgb_proba[i][0]:.4f}", f"{xgb_proba[i][1]:.4f}",
                int(ensemble_pred[i]),
                f"{ensemble_proba[i][0]:.4f}", f"{ensemble_proba[i][1]:.4f}",
            ])

    print(f"\n산출물 저장: {output_dir}/")
    print(f"  - xgb_model.pkl, rf_model.pkl, gb_model.pkl")
    print(f"  - preprocessors.pkl")
    print(f"  - metrics_report.json")
    print(f"  - metrics_report.md")
    print(f"  - test_predictions.csv ({len(y_te)}건)")
    print(f"  - feature_schema.md")
    print(f"\nXGB test accuracy: {xgb_acc:.4f}")
    print(f"앙상블 test accuracy: {ensemble_acc:.4f}")

    return results


def main():
    parser = argparse.ArgumentParser(description='Phase C 학습')
    parser.add_argument('--output-dir', default='models/phase_c', help='모델 출력 디렉토리')
    args = parser.parse_args()

    print("=" * 50)
    print("Phase C: 인용/기각 예측 모델 학습")
    print("=" * 50)
    print()

    src, tagged = load_data()
    records = build_dataset(src, tagged)
    X, y, pe, se, tfidf = build_features(records)

    # 전처리기도 저장 (서빙용)
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, 'preprocessors.pkl'), 'wb') as f:
        pickle.dump({'primary_encoder': pe, 'stage_encoder': se, 'tfidf': tfidf}, f)

    results = train_and_evaluate(X, y, args.output_dir)

    print("\n완료.")


if __name__ == '__main__':
    main()
