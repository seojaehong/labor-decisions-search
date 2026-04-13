/**
 * bc_ 임베딩 생성 v3 — holding_summary 없는 건을 key_issue + title로 임베딩
 *
 * v2가 holding_summary 있는 건만 처리하므로,
 * 이 스크립트는 holding_summary가 null이지만 key_issue가 있는 건을 처리
 */

const { createClient } = require("@supabase/supabase-js");
require("dotenv").config({ path: ".env.local" });

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_URL = "https://api.openai.com/v1/embeddings";
const EMBEDDING_MODEL = "text-embedding-3-small";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, {
  db: { schema: "public" },
  global: { headers: { "x-connection-pool": "true" } },
});

const OPENAI_BATCH = 100;
const DB_FETCH = 200;

async function getEmbeddings(texts) {
  const resp = await fetch(OPENAI_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${OPENAI_API_KEY}`,
    },
    body: JSON.stringify({ model: EMBEDDING_MODEL, input: texts }),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`OpenAI ${resp.status}: ${err.slice(0, 200)}`);
  }
  const data = await resp.json();
  return data.data.map((d) => d.embedding);
}

async function updateEmbedding(id, embedding) {
  const { error } = await supabase
    .from("nlrc_decisions")
    .update({ embedding })
    .eq("id", id);
  return error;
}

async function main() {
  if (!OPENAI_API_KEY) {
    console.error("No OPENAI_API_KEY");
    process.exit(1);
  }

  console.log("=== bc_ 임베딩 생성 v3 (key_issue 기반) ===");

  let done = 0,
    failed = 0,
    lastId = "";
  const startTime = Date.now();

  while (true) {
    // holding_summary가 null이지만 key_issue가 있는 bc_ 레코드
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("id, title, key_issue")
      .like("id", "bc_%")
      .is("embedding", null)
      .is("holding_summary", null)
      .not("key_issue", "is", null)
      .order("id")
      .gt("id", lastId || "")
      .limit(DB_FETCH);

    if (error) {
      console.error("DB fetch error:", error.message);
      break;
    }
    if (!data?.length) {
      console.log("\n완료!");
      break;
    }

    lastId = data[data.length - 1].id;

    for (let i = 0; i < data.length; i += OPENAI_BATCH) {
      const chunk = data.slice(i, i + OPENAI_BATCH);
      const texts = chunk.map(
        (r) => `${r.title || ""}\n${r.key_issue || ""}`
      );

      try {
        const embeddings = await getEmbeddings(texts);

        let batchOk = 0,
          batchFail = 0;
        for (let j = 0; j < chunk.length; j++) {
          const err = await updateEmbedding(chunk[j].id, embeddings[j]);
          if (err) {
            batchFail++;
            if (err.message?.includes("timeout")) {
              await new Promise((r) => setTimeout(r, 2000));
              const retryErr = await updateEmbedding(
                chunk[j].id,
                embeddings[j]
              );
              if (!retryErr) {
                batchFail--;
                batchOk++;
              }
            }
          } else {
            batchOk++;
          }
        }
        done += batchOk;
        failed += batchFail;
      } catch (apiErr) {
        console.error(`\nAPI error: ${apiErr.message}`);
        await new Promise((r) => setTimeout(r, 10000));
        continue;
      }

      const elapsed = (Date.now() - startTime) / 1000;
      const rate = done / elapsed;
      process.stdout.write(
        `\r✅ ${done} | ❌ ${failed} | ${rate.toFixed(1)}/s  `
      );
    }
  }

  console.log(`\n\n=== 결과 ===`);
  console.log(`성공: ${done}, 실패: ${failed}`);
  console.log(`소요: ${((Date.now() - startTime) / 1000 / 60).toFixed(1)}분`);
}

main().catch(console.error);
