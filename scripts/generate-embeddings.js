/**
 * document-level 임베딩 생성 스크립트
 *
 * holding_summary 기반 text-embedding-3-small (1536차원)
 * 42,105건 × 평균 481자 ≈ ~800K 토큰 → ~$0.02/1M → ~$1.5 예상
 *
 * 사용법:
 *   node scripts/generate-embeddings.js              # 전체 실행
 *   node scripts/generate-embeddings.js --limit 100  # 테스트
 *   node scripts/generate-embeddings.js --dry-run    # 비용만 확인
 */

const { createClient } = require("@supabase/supabase-js");
require("dotenv").config({ path: ".env.local" });

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_URL = "https://api.openai.com/v1/embeddings";
const EMBEDDING_MODEL = "text-embedding-3-small";
const EMBEDDING_DIM = 1536;

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

// CLI 인자
const args = process.argv.slice(2);
const DRY_RUN = args.includes("--dry-run");
const limitIdx = args.indexOf("--limit");
const LIMIT = limitIdx >= 0 ? parseInt(args[limitIdx + 1]) : null;

const BATCH_SIZE = 100; // OpenAI embedding API는 배치 지원
const DB_BATCH = 500;   // Supabase 조회 단위

async function getEmbeddings(texts) {
  const resp = await fetch(OPENAI_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${OPENAI_API_KEY}`,
    },
    body: JSON.stringify({
      model: EMBEDDING_MODEL,
      input: texts,
    }),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`OpenAI API ${resp.status}: ${err.slice(0, 200)}`);
  }

  const data = await resp.json();
  return data.data.map((d) => d.embedding);
}

async function main() {
  if (!OPENAI_API_KEY) {
    console.error("OPENAI_API_KEY가 설정되지 않았습니다.");
    process.exit(1);
  }

  console.log(`=== 임베딩 생성 (${EMBEDDING_MODEL}, ${EMBEDDING_DIM}차원) ===`);
  console.log(`모드: ${DRY_RUN ? "DRY RUN (비용 추정만)" : "LIVE"}`);
  if (LIMIT) console.log(`제한: ${LIMIT}건`);
  console.log("");

  let processed = 0;
  let updated = 0;
  let totalTokens = 0;
  let lastId = "";

  while (true) {
    if (LIMIT && processed >= LIMIT) break;

    const batchSize = LIMIT ? Math.min(DB_BATCH, LIMIT - processed) : DB_BATCH;

    // cursor 기반 페이지네이션 (embedding IS NULL 대신 id 순회 — 타임아웃 방지)
    let query = supabase
      .from("nlrc_decisions")
      .select("id, holding_summary, title, embedding")
      .not("holding_summary", "is", null)
      .order("id")
      .limit(batchSize);

    if (lastId) query = query.gt("id", lastId);

    const { data, error } = await query;
    if (error) {
      console.error("DB 에러:", error.message);
      break;
    }
    if (!data?.length) break;

    // 이미 임베딩이 있는 레코드 건너뛰기
    const needsEmbedding = data.filter((r) => !r.embedding);
    if (needsEmbedding.length === 0) {
      processed += data.length;
      lastId = data[data.length - 1].id;
      continue;
    }

    // 임베딩 텍스트 준비: title + holding_summary
    const texts = needsEmbedding.map(
      (r) => `${r.title || ""}\n${r.holding_summary || ""}`
    );
    // data를 needsEmbedding으로 교체 (아래 로직용)
    const workData = needsEmbedding;

    // 토큰 추정 (한국어 ~1.5자/토큰)
    const charCount = texts.reduce((s, t) => s + t.length, 0);
    const estTokens = Math.ceil(charCount / 1.5);
    totalTokens += estTokens;

    if (!DRY_RUN) {
      // OpenAI 배치 임베딩 (BATCH_SIZE씩 나눠서)
      for (let i = 0; i < texts.length; i += BATCH_SIZE) {
        const chunk = texts.slice(i, i + BATCH_SIZE);
        const chunkData = workData.slice(i, i + BATCH_SIZE);

        try {
          const embeddings = await getEmbeddings(chunk);

          // Supabase 업데이트 (개별)
          for (let j = 0; j < chunkData.length; j++) {
            const { error: updateErr } = await supabase
              .from("nlrc_decisions")
              .update({ embedding: embeddings[j] })
              .eq("id", chunkData[j].id);

            if (updateErr) {
              console.error(`  UPDATE 에러 [${chunkData[j].id}]: ${updateErr.message}`);
            } else {
              updated++;
            }
          }
        } catch (apiErr) {
          console.error(`  API 에러 (batch ${i}): ${apiErr.message}`);
          // rate limit 대비 대기
          await new Promise((r) => setTimeout(r, 5000));
        }
      }
    }

    processed += data.length;
    lastId = data[data.length - 1].id;

    const estCost = (totalTokens / 1_000_000) * 0.02;
    process.stdout.write(
      `\r처리: ${processed.toLocaleString()}건 | 업데이트: ${updated.toLocaleString()} | ~${totalTokens.toLocaleString()} 토큰 | ~$${estCost.toFixed(3)}`
    );
  }

  const finalCost = (totalTokens / 1_000_000) * 0.02;
  console.log("\n\n=== 결과 ===");
  console.log(`처리: ${processed.toLocaleString()}건`);
  console.log(`업데이트: ${updated.toLocaleString()}건`);
  console.log(`추정 토큰: ${totalTokens.toLocaleString()}`);
  console.log(`추정 비용: $${finalCost.toFixed(3)}`);
}

main().catch(console.error);
