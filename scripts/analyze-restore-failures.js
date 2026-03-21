#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
require("dotenv").config({ path: path.join(process.cwd(), ".env.local") });
require("dotenv").config({ path: path.join(process.cwd(), ".env") });
const { createClient } = require("@supabase/supabase-js");

const ROOT = process.cwd();
const SOURCE_JSON_PATH = "C:\\Users\\iceam\\OneDrive\\5.산업안전\\문서\\Obsidian Vault\\레퍼런스\\최영우\\법제처_노동위결정문_전문.json";
const FAILURE_LOG = path.join(ROOT, "scripts", "logs", "restore-from-source-failures.jsonl");
const REPORT_PATH = path.join(ROOT, "scripts", "logs", "restore-from-source-summary.md");

function getSourceKeyFromRow(row) {
  const url = typeof row.url === "string" ? row.url : "";
  const match = url.match(/[?&]ID=(\d+)/i);
  if (match?.[1]) return `id_${match[1]}`;
  if (typeof row.id === "string" && /^id_\d+$/i.test(row.id)) return row.id;
  return "";
}

async function loadAllRows(supabase) {
  const pageSize = 1000;
  let from = 0;
  const rows = [];
  while (true) {
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("id, url, case_number, holding_points")
      .order("id", { ascending: true })
      .range(from, from + pageSize - 1);
    if (error) throw error;
    if (!data || data.length === 0) break;
    rows.push(...data);
    if (data.length < pageSize) break;
    from += pageSize;
  }
  return rows;
}

function loadFailureIds() {
  const ids = new Set();
  if (!fs.existsSync(FAILURE_LOG)) return ids;
  const lines = fs.readFileSync(FAILURE_LOG, "utf8").split(/\r?\n/).filter(Boolean);
  for (const line of lines) {
    try {
      const parsed = JSON.parse(line);
      if (parsed?.id) ids.add(parsed.id);
    } catch {
      // ignore malformed log lines
    }
  }
  return ids;
}

function summarizeFailure(row, entry) {
  const sourceKey = getSourceKeyFromRow(row);
  if (!sourceKey) return { code: "missing_source_key", sourceKey: "" };
  if (!entry) return { code: "missing_source_entry", sourceKey };

  const yoji = String(entry["판정요지"] || "").trim();
  const content = String(entry["내용"] || "").trim();
  const caseNumber = String(entry["사건번호"] || entry.caseNumber || "").trim();

  if (yoji && yoji.length < 100) {
    return {
      code: "holding_short_from_yoji",
      sourceKey,
      yojiLength: yoji.length,
      contentLength: content.length,
      hasCaseNumber: Boolean(caseNumber),
    };
  }
  if (!yoji && content && content.length < 100) {
    return {
      code: "holding_short_from_content_fallback",
      sourceKey,
      yojiLength: 0,
      contentLength: content.length,
      hasCaseNumber: Boolean(caseNumber),
    };
  }
  if (!yoji && !content) {
    return {
      code: "holding_missing",
      sourceKey,
      yojiLength: 0,
      contentLength: 0,
      hasCaseNumber: Boolean(caseNumber),
    };
  }
  if (!caseNumber) {
    return {
      code: "case_number_missing",
      sourceKey,
      yojiLength: yoji.length,
      contentLength: content.length,
      hasCaseNumber: false,
    };
  }
  return {
    code: "other",
    sourceKey,
    yojiLength: yoji.length,
    contentLength: content.length,
    hasCaseNumber: Boolean(caseNumber),
  };
}

async function main() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    { auth: { persistSession: false } }
  );

  const sourceMap = JSON.parse(fs.readFileSync(SOURCE_JSON_PATH, "utf8"));
  const failureIds = loadFailureIds();
  const allRows = await loadAllRows(supabase);

  const shortRows = allRows.filter((row) => ((row.holding_points || "").trim().length < 100));
  const failedRows = shortRows.filter((row) => failureIds.has(row.id));

  const byCode = {};
  const samples = {};

  for (const row of failedRows) {
    const sourceKey = getSourceKeyFromRow(row);
    const entry = sourceMap[sourceKey];
    const summary = summarizeFailure(row, entry);
    byCode[summary.code] = (byCode[summary.code] || 0) + 1;
    if (!samples[summary.code]) samples[summary.code] = [];
    if (samples[summary.code].length < 5) {
      samples[summary.code].push({
        id: row.id,
        case_number: row.case_number,
        source_key: sourceKey || "",
        holding_len: ((row.holding_points || "").trim().length),
        yojiLength: summary.yojiLength || 0,
        contentLength: summary.contentLength || 0,
      });
    }
  }

  const beforeShortHolding = 34956;
  const beforeIdCase = 41959;
  const currentIdCase = allRows.filter((row) => /^id_/i.test((row.case_number || "").trim())).length;

  const lines = [
    "# restore-from-source summary",
    "",
    `- total rows: ${allRows.length}`,
    `- short holding_points (<100): ${shortRows.length}`,
    `- short holding_points before: ${beforeShortHolding}`,
    `- reduced short holdings: ${beforeShortHolding - shortRows.length}`,
    `- id_ case_number before: ${beforeIdCase}`,
    `- id_ case_number now: ${currentIdCase}`,
    `- reduced id_ case_number: ${beforeIdCase - currentIdCase}`,
    `- failed short rows tracked in failure log: ${failedRows.length}`,
    "",
    "## Failure buckets",
    "",
    ...Object.entries(byCode)
      .sort((a, b) => b[1] - a[1])
      .map(([code, count]) => `- ${code}: ${count}`),
    "",
    "## Sample rows",
    "",
  ];

  for (const [code, items] of Object.entries(samples)) {
    lines.push(`### ${code}`);
    lines.push("");
    for (const item of items) {
      lines.push(`- ${item.id} | case_number=${item.case_number || "(none)"} | source_key=${item.source_key || "(none)"} | holding_len=${item.holding_len} | yoji=${item.yojiLength} | content=${item.contentLength}`);
    }
    lines.push("");
  }

  fs.mkdirSync(path.dirname(REPORT_PATH), { recursive: true });
  fs.writeFileSync(REPORT_PATH, `${lines.join("\n")}\n`, "utf8");
  console.log(JSON.stringify({ report: REPORT_PATH, byCode, shortRows: shortRows.length, currentIdCase }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
