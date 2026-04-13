import { createClient } from "@supabase/supabase-js";

function readArg(flag, fallback = undefined) {
  const index = process.argv.indexOf(flag);
  if (index === -1) return fallback;
  return process.argv[index + 1] ?? fallback;
}

function resolveEnv() {
  const url =
    process.env.SUPABASE_URL ||
    process.env.NEXT_PUBLIC_SUPABASE_URL ||
    "https://mewqgevgdgghhatqtuos.supabase.co";

  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ||
    process.env.SUPABASE_SERVICE_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  return { url, key };
}

function bucketDecisionResult(result) {
  if (["granted", "overturned", "전부인정", "인정"].includes(result)) return "granted";
  if (["partial", "일부인정"].includes(result)) return "partial";
  if (["dismissed", "rejected", "upheld", "기각", "각하", "초심유지"].includes(result)) return "dismissed";
  return "other";
}

function printCases(label, rows) {
  console.log(`\n[${label}] ${rows.length}건`);
  for (const row of rows) {
    const categories = Array.isArray(row.reason_category) ? row.reason_category.join(", ") : "";
    console.log(
      `- ${row.decision_result.padEnd(10)} | ${String(row.relevance ?? "").slice(0, 6).padEnd(6)} | ${row.case_number || "-"} | ${row.title}`
    );
    if (categories) {
      console.log(`  reason_category: ${categories}`);
    }
  }
}

async function runQuery(supabase, payload) {
  const { data, error } = await supabase.rpc("search_similar_cases", payload);
  if (error) {
    throw error;
  }

  const rows = data ?? [];
  const summary = rows.reduce(
    (acc, row) => {
      const bucket = bucketDecisionResult(row.decision_result);
      acc[bucket] = (acc[bucket] || 0) + 1;
      return acc;
    },
    { granted: 0, dismissed: 0, partial: 0, other: 0 }
  );

  return { rows, summary };
}

async function main() {
  const { url, key } = resolveEnv();
  const query = readArg("--query");
  const category = readArg("--category", null);
  const limit = Number(readArg("--limit", "4"));

  if (!key) {
    console.error("Missing Supabase key. Set SUPABASE_SERVICE_ROLE_KEY, SUPABASE_SERVICE_KEY, or NEXT_PUBLIC_SUPABASE_ANON_KEY.");
    process.exit(1);
  }

  const supabase = createClient(url, key, { auth: { persistSession: false } });

  const testCases = query
    ? [{ query, category, limit }]
    : [
        { query: "직원이 3일간 무단결근하여 해고했습니다", category: "부당해고", limit },
        { query: "노조 가입을 이유로 불이익을 줬습니다", category: "부당노동행위", limit },
      ];

  for (const testCase of testCases) {
    console.log(`\n=== query: ${testCase.query}`);
    if (testCase.category) {
      console.log(`category: ${testCase.category}`);
    }
    console.log(`limit(per bucket): ${testCase.limit}`);

    const result = await runQuery(supabase, {
      query: testCase.query,
      category: testCase.category,
      limit: testCase.limit,
    });

    console.log(
      `summary: granted=${result.summary.granted}, dismissed=${result.summary.dismissed}, partial=${result.summary.partial}, other=${result.summary.other}`
    );

    printCases("results", result.rows);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
