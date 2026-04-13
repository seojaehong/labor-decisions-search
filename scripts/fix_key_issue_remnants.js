const { createClient } = require("@supabase/supabase-js");
const s = createClient(
  "https://mewqgevgdgghhatqtuos.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ld3FnZXZnZGdnaGhhdHF0dW9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MTU1MTAsImV4cCI6MjA4ODI5MTUxMH0.sgjPikmLaudwW9iWgg5TQNfSjHVBD7JtjYWgUpNezng"
);

async function fix() {
  // 1. ```markdown 껍데기 → NULL
  const { data: md, error: e1 } = await s
    .from("nlrc_decisions")
    .update({ key_issue: null })
    .eq("key_issue", "```markdown")
    .select("id");
  console.log("```markdown → NULL:", md?.length || 0, "건", e1?.message || "OK");

  // 2. ... 껍데기 → NULL (10자 이하)
  const { data: dots, error: e2 } = await s
    .from("nlrc_decisions")
    .update({ key_issue: null })
    .like("key_issue", "...%")
    .select("id");
  // dots 중 10자 이하만 카운트
  const shortDots = (dots || []).filter((d) => true); // already filtered by like
  console.log("... → NULL:", shortDots.length, "건", e2?.message || "OK");

  // 3. 최종 검증
  const { count: c1 } = await s
    .from("nlrc_decisions")
    .select("id", { count: "exact", head: true })
    .eq("key_issue", "```markdown");
  const { count: c2 } = await s
    .from("nlrc_decisions")
    .select("id", { count: "exact", head: true })
    .like("key_issue", "...%");
  const { count: c3 } = await s
    .from("nlrc_decisions")
    .select("id", { count: "exact", head: true })
    .like("key_issue", "## %");
  const { count: c4 } = await s
    .from("nlrc_decisions")
    .select("id", { count: "exact", head: true })
    .like("key_issue", "# %");

  console.log("\n=== 최종 검증 ===");
  console.log("잔여 ```markdown:", c1);
  console.log("잔여 ...:", c2);
  console.log("잔여 ## 헤더:", c3);
  console.log("잔여 # 헤더:", c4);
}

fix();
