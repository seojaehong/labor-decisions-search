/**
 * 38k 확장 배치 생성 스크립트
 *
 * DB에서 미태깅 케이스를 추출하여 Tier별 배치 파일 생성.
 * 케이스당 중복 없이 1회만 포함.
 *
 * 사용법:
 *   node scripts/generate_38k_batches.js                    # 전체 Tier 1-2
 *   node scripts/generate_38k_batches.js --tier 1           # Tier 1만
 *   node scripts/generate_38k_batches.js --tier 2           # Tier 2만
 *   node scripts/generate_38k_batches.js --dry-run          # 건수만 확인
 */

const { createClient } = require("@supabase/supabase-js");
const fs = require("fs");
const path = require("path");
require("dotenv").config({ path: ".env.local" });

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

const BATCH_SIZE = 50;
const OUTPUT_DIR = "retagging/input/batches_38k";

// 이미 태깅된 case_id 목록
function loadTaggedIds() {
  const mergedPath = "retagging/output/merged/merged_final_v2.jsonl";
  const ids = new Set();
  if (fs.existsSync(mergedPath)) {
    for (const line of fs.readFileSync(mergedPath, "utf-8").split("\n")) {
      if (line.trim()) {
        try { ids.add(JSON.parse(line).case_id); } catch {}
      }
    }
  }
  return ids;
}

// Tier 정의
const TIERS = {
  1: [
    { name: "transfer", reasons: ["transfer"], hint: "전보/전직/대기발령 정당성" },
    { name: "contract_expiry", reasons: ["contract_expiry"], hint: "갱신기대권/계약만료" },
    { name: "sexual_harassment", reasons: ["sexual_harassment"], hint: "성희롱 징계" },
  ],
  2: [
    { name: "misconduct_remaining", reasons: ["misconduct"], hint: "복합비위/misconduct vs disciplinary_severity" },
    { name: "union_activity", reasons: ["union_activity"], hint: "부당노동행위/노조 관련" },
    { name: "redundancy", reasons: ["redundancy"], hint: "경영상 해고/정리해고" },
    { name: "discrimination", reasons: ["discrimination"], hint: "차별시정" },
  ],
};

const args = process.argv.slice(2);
const DRY_RUN = args.includes("--dry-run");
const tierArg = args.indexOf("--tier");
const TARGET_TIER = tierArg >= 0 ? parseInt(args[tierArg + 1]) : 0; // 0 = all

async function main() {
  console.log("=== 38k 확장 배치 생성 ===\n");

  // 이미 태깅된 ID 로드
  const taggedIds = loadTaggedIds();
  console.log(`이미 태깅: ${taggedIds.size}건\n`);

  // 출력 디렉토리
  if (!DRY_RUN) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const tiers = TARGET_TIER ? { [TARGET_TIER]: TIERS[TARGET_TIER] } : TIERS;
  let totalBatches = 0;
  let totalCases = 0;
  const processedIds = new Set(); // 중복 방지

  for (const [tierNum, groups] of Object.entries(tiers)) {
    console.log(`\n--- Tier ${tierNum} ---`);

    for (const group of groups) {
      console.log(`\n[${group.name}] reasons: ${group.reasons.join(", ")}`);

      // DB에서 해당 reason_category 케이스 추출
      let allCases = [];
      let lastId = "";

      while (true) {
        let query = supabase
          .from("nlrc_decisions")
          .select("id, title, decision_result, sanction_type, reason_category, tags, holding_points, holding_summary")
          .overlaps("reason_category", group.reasons)
          .not("holding_summary", "is", null)
          .order("id")
          .limit(1000);

        if (lastId) query = query.gt("id", lastId);

        const { data, error } = await query;
        if (error) { console.error("DB 에러:", error.message); break; }
        if (!data?.length) break;

        for (const r of data) {
          // 이미 태깅된 건 제외
          if (taggedIds.has(r.id)) continue;
          // 이 실행에서 이미 처리한 건 제외 (중복 방지)
          if (processedIds.has(r.id)) continue;

          processedIds.add(r.id);
          allCases.push(r);
        }

        lastId = data[data.length - 1].id;
        if (data.length < 1000) break;
      }

      console.log(`  추출: ${allCases.length}건 (중복 제외)`);

      if (DRY_RUN) {
        totalCases += allCases.length;
        totalBatches += Math.ceil(allCases.length / BATCH_SIZE);
        continue;
      }

      // 배치 분할 + 저장
      let batchNum = 1;
      for (let i = 0; i < allCases.length; i += BATCH_SIZE) {
        const batch = allCases.slice(i, i + BATCH_SIZE);
        const lines = batch.map((r) =>
          JSON.stringify({
            case_id: r.id,
            case_name: r.title,
            source_text: r.holding_summary,
            holding_points: r.holding_points,
            decision_result: r.decision_result,
            sanction_type: r.sanction_type,
            legacy_reason_category: r.reason_category,
            tags: r.tags,
            tagging_hint: group.hint,
          })
        );

        const fname = path.join(
          OUTPUT_DIR,
          `${group.name}_batch_${String(batchNum).padStart(3, "0")}.jsonl`
        );
        fs.writeFileSync(fname, lines.join("\n") + "\n");
        batchNum++;
      }

      const batchCount = batchNum - 1;
      totalBatches += batchCount;
      totalCases += allCases.length;
      console.log(`  → ${batchCount}개 배치 생성 (${BATCH_SIZE}건/배치)`);
    }
  }

  console.log(`\n${"=".repeat(50)}`);
  console.log(`총 케이스: ${totalCases}건`);
  console.log(`총 배치: ${totalBatches}개`);
  console.log(`중복 제외 처리: ${processedIds.size}건`);
  if (DRY_RUN) console.log("(dry-run, 파일 미생성)");
}

main().catch(console.error);
