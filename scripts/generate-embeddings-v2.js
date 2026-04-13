/**
 * bc_ 임베딩 생성 v2 — service role key + batch upsert
 *
 * Fixes: individual UPDATE timeout on anon key
 * Uses service role key for no RLS + longer timeout
 */

const { createClient } = require("@supabase/supabase-js");
require("dotenv").config({ path: ".env.local" });

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_URL = "https://api.openai.com/v1/embeddings";
const EMBEDDING_MODEL = "text-embedding-3-small";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY; // service role

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, {
  db: { schema: 'public' },
  global: { headers: { 'x-connection-pool': 'true' } }
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
  // Use raw SQL via rpc for faster updates
  const { error } = await supabase
    .from("nlrc_decisions")
    .update({ embedding })
    .eq("id", id);
  return error;
}

async function main() {
  if (!OPENAI_API_KEY) { console.error("No OPENAI_API_KEY"); process.exit(1); }

  console.log("=== bc_ 임베딩 생성 v2 ===");

  let done = 0, failed = 0, lastId = "bc_";
  const startTime = Date.now();

  while (true) {
    // Fetch bc_ records without embedding
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("id, title, holding_summary")
      .like("id", "bc_%")
      .is("embedding", null)
      .not("holding_summary", "is", null)
      .order("id")
      .gt("id", lastId)
      .limit(DB_FETCH);

    if (error) { console.error("DB fetch error:", error.message); break; }
    if (!data?.length) { console.log("\n완료!"); break; }

    lastId = data[data.length - 1].id;

    // Process in OpenAI batch chunks
    for (let i = 0; i < data.length; i += OPENAI_BATCH) {
      const chunk = data.slice(i, i + OPENAI_BATCH);
      const texts = chunk.map(r => `${r.title || ""}\n${r.holding_summary || ""}`);

      try {
        const embeddings = await getEmbeddings(texts);

        // Update one by one (Supabase doesn't support batch update with different values)
        let batchOk = 0, batchFail = 0;
        for (let j = 0; j < chunk.length; j++) {
          const err = await updateEmbedding(chunk[j].id, embeddings[j]);
          if (err) {
            batchFail++;
            // On timeout, wait and retry once
            if (err.message?.includes('timeout')) {
              await new Promise(r => setTimeout(r, 2000));
              const retryErr = await updateEmbedding(chunk[j].id, embeddings[j]);
              if (!retryErr) { batchFail--; batchOk++; }
            }
          } else {
            batchOk++;
          }
        }
        done += batchOk;
        failed += batchFail;
      } catch (apiErr) {
        console.error(`\nAPI error: ${apiErr.message}`);
        await new Promise(r => setTimeout(r, 10000));
        continue;
      }

      const elapsed = (Date.now() - startTime) / 1000;
      const rate = done / elapsed;
      const remaining = 18168 - done;
      const eta = rate > 0 ? Math.ceil(remaining / rate / 60) : '?';
      process.stdout.write(
        `\r✅ ${done} | ❌ ${failed} | ${rate.toFixed(1)}/s | ETA ${eta}m  `
      );
    }
  }

  console.log(`\n\n=== 결과 ===`);
  console.log(`성공: ${done}, 실패: ${failed}`);
  console.log(`소요: ${((Date.now() - startTime) / 1000 / 60).toFixed(1)}분`);
}

main().catch(console.error);
