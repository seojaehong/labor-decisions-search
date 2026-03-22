# Phase C Metrics Report

- Date: 2026-03-22T19:03:26.157178
- Seed: 42
- Samples: 35752 (인용 11433 / 기각 24319)
- Features: 505

## Accuracy

| Model | Test Accuracy |
|-------|:---:|
| XGB | **0.8922** |
| Ensemble | 0.8869 |

## XGB Classification Report

              precision    recall  f1-score   support

          기각       0.92      0.92      0.92      4864
          인용       0.84      0.82      0.83      2287

    accuracy                           0.89      7151
   macro avg       0.88      0.87      0.88      7151
weighted avg       0.89      0.89      0.89      7151

## Ensemble Classification Report

              precision    recall  f1-score   support

          기각       0.90      0.94      0.92      4864
          인용       0.86      0.77      0.81      2287

    accuracy                           0.89      7151
   macro avg       0.88      0.86      0.87      7151
weighted avg       0.89      0.89      0.89      7151
