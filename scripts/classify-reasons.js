/**
 * 키워드 패턴 기반 reason_category + sanction_type 일괄 분류
 *
 * API 호출 없이 holding_summary + tags 텍스트 패턴 매칭으로 분류
 * Claude Code에서 직접 실행: node scripts/classify-reasons.js [--dry-run] [--limit N]
 */

const { createClient } = require("@supabase/supabase-js");
require("dotenv").config({ path: ".env.local" });

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
console.log("Supabase URL:", url?.slice(0, 30) + "...");
console.log("Key:", key ? key.slice(0, 20) + "..." : "MISSING");
const supabase = createClient(url, key);

// === Step 1: 태그 기반 분류 (가장 신뢰도 높음) ===
const TAG_TO_REASON = {
  "성희롱": "sexual_harassment",
  "직장내괴롭힘": "workplace_bullying",
  "수습": "probation",
  "전보": "transfer",
  "갱신기대권": "contract_expiry",
  "해고부존재": "no_dismissal",
  "사직": "no_dismissal",
  "권고사직": "no_dismissal",
  "부당노동행위": "union_activity",
  "지배개입": "union_activity",
  "불이익취급": "union_activity",
  "근로자성": "worker_status",
  "당사자적격": "worker_status",
  "차별시정": "discrimination",
};

// === Step 2: 텍스트 패턴 기반 분류 (holding_summary 스캔) ===
const REASON_PATTERNS = [
  { category: "sexual_harassment", patterns: [/성희롱/, /성추행/, /성적\s*언동/, /성폭력/] },
  { category: "workplace_bullying", patterns: [/직장\s*내\s*괴롭힘/, /괴롭힘\s*행위/, /따돌림/] },
  { category: "violence", patterns: [/폭언/, /폭행/, /욕설.*징계/, /협박/, /위협.*행위/, /가혹행위/, /모욕/] },
  { category: "absence", patterns: [/무단결근/, /무단\s*이탈/, /연락\s*두절/, /근태\s*불량/, /무단\s*지각/, /근무\s*태만/, /결근/] },
  { category: "embezzlement", patterns: [/횡령/, /배임/, /착복/, /공금\s*유용/, /금전\s*비위/, /부정\s*수령/, /사금고/, /부정\s*청구/] },
  { category: "incompetence", patterns: [/업무능력\s*부족/, /근무성적\s*불량/, /업무\s*부적격/, /업무수행능력/, /실적\s*최하위/, /부적격\s*평가/] },
  { category: "probation", patterns: [/수습\s*기간/, /시용\s*근로자/, /수습\s*평가/, /본채용\s*거부/, /시용\s*해고/, /시용/] },
  { category: "redundancy", patterns: [/경영상\s*(해고|이유)/, /정리해고/, /구조조정/, /통폐합/, /경영\s*악화/, /인원\s*감축/, /사업\s*폐지/] },
  { category: "transfer", patterns: [/전보\s*(처분|조치|발령)/, /전직\s*(처분|발령|의\s*정당)/, /인사\s*발령/, /보직\s*변경/, /전배/, /전직명령/] },
  { category: "misconduct", patterns: [/복무규정\s*위반/, /음주운전/, /정보\s*유출/, /비위\s*행위/, /업무\s*지시\s*불이행/, /복종\s*의무\s*위반/, /겸직/, /허위\s*보고/] },
  // 징계사유 존재 + 해고사유 태그 → 일반 misconduct로 분류
  { category: "misconduct", patterns: [/징계사유.*인정/, /징계사유가\s*존재/] },
  // 새 5개 카테고리
  { category: "contract_expiry", patterns: [/갱신\s*기대권/, /계약\s*만료/, /기간제/, /근로계약\s*기간/, /재계약/, /계약\s*갱신/] },
  { category: "no_dismissal", patterns: [/해고.*존재하지/, /해고가\s*존재하지/, /해고\s*부존재/, /자발적.*사직/, /사직서.*제출/, /권고\s*사직/, /합의\s*퇴직/] },
  { category: "union_activity", patterns: [/부당노동행위/, /노조\s*활동/, /지배\s*개입/, /불이익\s*취급/, /조합\s*활동/] },
  { category: "worker_status", patterns: [/근로자.*해당하는지/, /근로자성/, /근로기준법상\s*근로자/, /위임\s*계약/, /도급\s*계약/] },
  { category: "discrimination", patterns: [/차별\s*시정/, /차별적\s*처우/, /비교\s*대상\s*근로자/] },
];

// === sanction_type 분류 패턴 ===
const SANCTION_PATTERNS = [
  { type: "suspension", patterns: [/정직/] },
  { type: "pay_cut", patterns: [/감봉/] },
  { type: "warning", patterns: [/경고/, /견책/, /주의\s*처분/, /훈계/] },
  { type: "demotion", patterns: [/강등/] },
  // dismissal은 기본값 (해고/파면/면직)
];

// === sanction_months 추출 패턴 ===
const MONTHS_PATTERNS = [
  // "정직 3월", "정직 3개월", "정직3월"
  /정직\s*(\d+)\s*(?:개월|월)/,
  /감봉\s*(\d+)\s*(?:개월|월)/,
  // "3개월 정직", "3개월의 정직", "3개월 정직처분", "1개월 임의 정직처분"
  /(\d+)\s*(?:개월|월)\s*(?:의\s*)?(?:임의\s*)?정직/,
  /(\d+)\s*(?:개월|월)\s*(?:의\s*)?감봉/,
  // "정직 처분 3월", "감봉처분 2월" (처분 뒤에 숫자)
  /정직\s*(?:처분)?\s*(\d+)\s*(?:개월|월)/,
  /감봉\s*(?:처분)?\s*(\d+)\s*(?:개월|월)/,
];

function classifyRecord(record) {
  const text = [
    record.title || "",
    record.holding_summary || "",
    record.holding_points || "",
    (record.tags || []).join(" "),
  ].join(" ");

  // 1. reason_category (복수 가능)
  const reasons = new Set();

  // Step 1: 태그 기반 (가장 신뢰도 높음)
  for (const tag of (record.tags || [])) {
    if (TAG_TO_REASON[tag]) reasons.add(TAG_TO_REASON[tag]);
  }

  // Step 2: 텍스트 패턴 기반 (보강)
  for (const { category, patterns } of REASON_PATTERNS) {
    for (const pattern of patterns) {
      if (pattern.test(text)) {
        reasons.add(category);
        break;
      }
    }
  }

  // 빈 경우 other
  if (reasons.size === 0) reasons.add("other");

  // 2. sanction_type
  let sanctionType = record.sanction_type || "dismissal"; // 기존값 유지 기본
  for (const { type, patterns } of SANCTION_PATTERNS) {
    for (const pattern of patterns) {
      if (pattern.test(text)) {
        sanctionType = type;
        break;
      }
    }
    if (sanctionType !== "dismissal" && sanctionType !== record.sanction_type) break;
  }

  // 3. sanction_months
  let sanctionMonths = null;
  for (const pattern of MONTHS_PATTERNS) {
    const match = text.match(pattern);
    if (match) {
      sanctionMonths = parseInt(match[1]);
      break;
    }
  }

  return {
    reason_category: [...reasons],
    sanction_type: sanctionType,
    sanction_months: sanctionMonths,
  };
}

// CLI 인자
const args = process.argv.slice(2);
const DRY_RUN = args.includes("--dry-run");
const limitIdx = args.indexOf("--limit");
const LIMIT = limitIdx >= 0 ? parseInt(args[limitIdx + 1]) : null;
const STATS_ONLY = args.includes("--stats");

async function main() {
  console.log(`=== 판정례 분류 (키워드 패턴) ===`);
  console.log(`모드: ${DRY_RUN ? "DRY RUN" : "LIVE"}`);
  if (LIMIT) console.log(`제한: ${LIMIT}건`);
  console.log("");

  console.log(`미분류 건 배치 처리 시작...\n`);

  const BATCH = 500;
  let processed = 0;
  let updated = 0;
  let lastId = "";
  const stats = {};
  const sanctionStats = {};

  while (true) {
    if (LIMIT && processed >= LIMIT) break;

    const batchSize = LIMIT ? Math.min(BATCH, LIMIT - processed) : BATCH;

    // cursor 기반 페이지네이션 (offset 대신 id 기반 - 타임아웃 방지)
    let query = supabase
      .from("nlrc_decisions")
      .select("id,title,holding_summary,holding_points,tags,sanction_type")
      .eq("reason_category", "{}")
      .order("id")
      .limit(batchSize);

    if (lastId) query = query.gt("id", lastId);

    const { data, error } = await query;

    if (error) { console.error("\nDB에러:", error.message); break; }
    if (!data?.length) break;

    const updates = [];

    for (const record of data) {
      const result = classifyRecord(record);

      // 통계 집계
      for (const r of result.reason_category) {
        stats[r] = (stats[r] || 0) + 1;
      }
      sanctionStats[result.sanction_type] = (sanctionStats[result.sanction_type] || 0) + 1;
      if (result.sanction_months) {
        const key = `${result.sanction_type}_${result.sanction_months}m`;
        sanctionStats[key] = (sanctionStats[key] || 0) + 1;
      }

      updates.push({
        id: record.id,
        reason_category: result.reason_category,
        sanction_type: result.sanction_type,
        sanction_months: result.sanction_months,
      });
    }

    if (!DRY_RUN && !STATS_ONLY) {
      // 배치 업데이트
      for (const u of updates) {
        const { error: updateErr } = await supabase
          .from("nlrc_decisions")
          .update({
            reason_category: u.reason_category,
            sanction_type: u.sanction_type,
            ...(u.sanction_months != null && { sanction_months: u.sanction_months }),
          })
          .eq("id", u.id);

        if (updateErr) {
          console.error(`  UPDATE 에러 [${u.id}]: ${updateErr.message}`);
        } else {
          updated++;
        }
      }
    }

    processed += data.length;
    lastId = data[data.length - 1].id;

    process.stdout.write(`\r처리: ${processed.toLocaleString()}건 | 업데이트: ${updated.toLocaleString()}`);
  }

  console.log("\n\n=== 분류 결과 통계 ===");
  console.log("\n[reason_category]");
  const sortedStats = Object.entries(stats).sort((a, b) => b[1] - a[1]);
  for (const [k, v] of sortedStats) {
    console.log(`  ${k}: ${v.toLocaleString()}건 (${((v / processed) * 100).toFixed(1)}%)`);
  }

  console.log("\n[sanction_type]");
  const sortedSanction = Object.entries(sanctionStats).sort((a, b) => b[1] - a[1]);
  for (const [k, v] of sortedSanction) {
    console.log(`  ${k}: ${v.toLocaleString()}건`);
  }

  console.log(`\n처리: ${processed}건 | 업데이트: ${updated}건`);
}

main().catch(console.error);
