/**
 * fix_key_issue_dump.js
 * bc_ 소스의 key_issue 전문 덤프 752건 정리
 *
 * 수정 로직:
 * 1. key_issue가 "# "으로 시작 → 첫 줄에서 # 제거 후 200자 이내 추출
 * 2. "## 결과 요약" 또는 "## 사실관계" 포함 → 첫 번째 줄만 추출
 * 3. 첫 줄이 10자 미만이면 두 번째 줄까지 합쳐서 사용
 *
 * 사용법:
 *   node scripts/fix_key_issue_dump.js          # DRY RUN (처음 10건 미리보기)
 *   node scripts/fix_key_issue_dump.js --apply  # 실제 UPDATE
 */

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://mewqgevgdgghhatqtuos.supabase.co';
const SUPABASE_ANON_KEY =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ld3FnZXZnZGdnaGhhdHF0dW9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTU1MTAsImV4cCI6MjA4ODI5MTUxMH0.sgjPikmLaudwW9iWgg5TQNfSjHVBD7JtjYWgUpNezng';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const APPLY = process.argv.includes('--apply');
const PAGE_SIZE = 1000;

/**
 * key_issue에서 정제된 한 줄 요약 추출
 */
function cleanKeyIssue(raw) {
  if (!raw) return raw;

  const lines = raw
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l.length > 0);

  if (lines.length === 0) return raw;

  let firstLine = lines[0];

  // 코드블록 펜스(```markdown, ``` 등) 또는 HTML/XML 태그 같은 메타라인 건너뛰기
  // 실제 내용(# 헤딩 또는 일반 텍스트) 첫 줄 찾기
  if (/^```/.test(firstLine) || /^<[^>]+>$/.test(firstLine)) {
    for (let idx = 1; idx < lines.length; idx++) {
      const candidate = lines[idx];
      // 펜스나 순수 태그가 아닌 첫 줄 선택
      if (!/^```/.test(candidate) && !/^<[^>]+>$/.test(candidate)) {
        firstLine = candidate;
        break;
      }
    }
  }

  // # 헤딩 제거
  firstLine = firstLine.replace(/^#+\s*/, '').trim();

  // 첫 줄이 10자 미만이면 두 번째 줄 합치기
  if (firstLine.length < 10 && lines.length > 1) {
    let secondLine = lines[1].replace(/^#+\s*/, '').trim();
    // 두 번째 줄도 섹션 헤더(## 결과 요약 등)면 건너뜀
    if (/^(결과\s*요약|사실관계|판단|주문|이유)/.test(secondLine) && lines.length > 2) {
      secondLine = lines[2].replace(/^#+\s*/, '').trim();
    }
    firstLine = `${firstLine} ${secondLine}`.trim();
  }

  // 200자 이내로 자르기
  if (firstLine.length > 200) {
    firstLine = firstLine.slice(0, 200);
  }

  return firstLine;
}

/**
 * 수정 대상 여부 확인
 */
function needsFix(keyIssue) {
  if (!keyIssue) return false;
  return keyIssue.startsWith('# ') || keyIssue.includes('## ');
}

// BigCase 소스명 목록 (실제 DB 값 기준)
const BC_SOURCES = ['bigcase', 'bigcase.ai'];

async function fetchAllTargets() {
  const results = [];

  for (const source of BC_SOURCES) {
    let from = 0;

    // "## " 포함된 bigcase 소스 레코드 조회
    while (true) {
      const { data, error } = await supabase
        .from('nlrc_decisions')
        .select('id, key_issue')
        .eq('source', source)
        .ilike('key_issue', '%## %')
        .range(from, from + PAGE_SIZE - 1);

      if (error) {
        console.error('조회 오류:', error.message);
        process.exit(1);
      }

      if (!data || data.length === 0) break;
      results.push(...data);
      if (data.length < PAGE_SIZE) break;
      from += PAGE_SIZE;
    }

    // "# "으로 시작하는 케이스도 추가 조회 (위에서 안 잡힌 것)
    from = 0;
    while (true) {
      const { data, error } = await supabase
        .from('nlrc_decisions')
        .select('id, key_issue')
        .eq('source', source)
        .like('key_issue', '# %')
        .range(from, from + PAGE_SIZE - 1);

      if (error) {
        console.error('조회 오류:', error.message);
        process.exit(1);
      }

      if (!data || data.length === 0) break;
      // 중복 제거
      const existingIds = new Set(results.map((r) => r.id));
      for (const row of data) {
        if (!existingIds.has(row.id)) results.push(row);
      }
      if (data.length < PAGE_SIZE) break;
      from += PAGE_SIZE;
    }
  }

  return results;
}

async function main() {
  console.log('='.repeat(60));
  console.log('key_issue 전문 덤프 정리 스크립트');
  console.log(`모드: ${APPLY ? '실제 UPDATE' : 'DRY RUN (미리보기)'}`);
  console.log('='.repeat(60));

  console.log('\n대상 레코드 조회 중...');
  const targets = await fetchAllTargets();
  console.log(`총 대상: ${targets.length}건`);

  if (targets.length === 0) {
    console.log('수정 대상 없음. 종료합니다.');
    return;
  }

  // 변경 전/후 비교 (처음 10건)
  console.log('\n[DRY RUN 미리보기 — 처음 10건]');
  console.log('-'.repeat(60));

  const preview = targets.slice(0, 10);
  for (const row of preview) {
    const cleaned = cleanKeyIssue(row.key_issue);
    console.log(`\nID: ${row.id}`);
    console.log(`  변경 전: ${row.key_issue.slice(0, 120).replace(/\n/g, '↵')}...`);
    console.log(`  변경 후: ${cleaned}`);
  }

  console.log('\n' + '-'.repeat(60));

  if (!APPLY) {
    console.log('\n[DRY RUN 완료]');
    console.log(`실제 적용하려면: node scripts/fix_key_issue_dump.js --apply`);
    return;
  }

  // 실제 UPDATE
  console.log('\n실제 UPDATE 시작...');

  let successCount = 0;
  let errorCount = 0;
  const BATCH_SIZE = 100;

  for (let i = 0; i < targets.length; i += BATCH_SIZE) {
    const batch = targets.slice(i, i + BATCH_SIZE);

    // 각 레코드 개별 update (upsert 미사용 — id 기준 단순 update)
    const promises = batch.map(async (row) => {
      const cleaned = cleanKeyIssue(row.key_issue);
      const { error } = await supabase
        .from('nlrc_decisions')
        .update({ key_issue: cleaned })
        .eq('id', row.id);

      if (error) {
        console.error(`  [ERROR] id=${row.id}: ${error.message}`);
        return false;
      }
      return true;
    });

    const results = await Promise.all(promises);
    successCount += results.filter(Boolean).length;
    errorCount += results.filter((r) => !r).length;

    const done = Math.min(i + BATCH_SIZE, targets.length);
    process.stdout.write(`  진행: ${done}/${targets.length} (성공 ${successCount}, 오류 ${errorCount})\r`);
  }

  console.log('\n' + '='.repeat(60));
  console.log('UPDATE 완료');
  console.log(`  총 대상: ${targets.length}건`);
  console.log(`  성공: ${successCount}건`);
  console.log(`  오류: ${errorCount}건`);
  console.log('='.repeat(60));
}

main().catch((err) => {
  console.error('치명적 오류:', err);
  process.exit(1);
});
