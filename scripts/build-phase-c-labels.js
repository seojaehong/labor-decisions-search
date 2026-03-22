#!/usr/bin/env node
/**
 * Phase C 이진 라벨 데이터셋 생성기
 *
 * 규칙:
 * - granted, partial -> worker_win
 * - dismissed, rejected -> user_win
 * - upheld, overturned, other/null -> undecidable (보류)
 *
 * 실행:
 *   node scripts/build-phase-c-labels.js --dry-run --limit 50
 *   node scripts/build-phase-c-labels.js
 */

const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

const ROOT = path.resolve(__dirname, "..");

function initEnv() {
  try {
    require("dotenv").config({ path: path.join(ROOT, ".env.local"), quiet: true });
    require("dotenv").config({ path: path.join(ROOT, ".env"), quiet: true });
  } catch {
    // no-op
  }
}

initEnv();

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("Missing Supabase credentials");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, {
  auth: { persistSession: false, autoRefreshToken: false },
});

const DEFAULT_OUTPUT = path.join(ROOT, "retagging", "evaluation", "phase_c_labels_v1.jsonl");
const DEFAULT_REPORT = path.join(ROOT, "retagging", "evaluation", "phase_c_label_report.md");
const PAGE_SIZE = 1000;

function parseArgs(argv) {
  const args = {
    dryRun: false,
    limit: null,
    output: DEFAULT_OUTPUT,
    report: DEFAULT_REPORT,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--limit") {
      args.limit = Number(argv[i + 1]);
      i += 1;
    } else if (arg === "--output") {
      args.output = path.resolve(argv[i + 1]);
      i += 1;
    } else if (arg === "--report") {
      args.report = path.resolve(argv[i + 1]);
      i += 1;
    }
  }

  return args;
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function normalizeArray(value) {
  return Array.isArray(value) ? value : [];
}

const DIRECT_WORKER_WIN = new Set([
  "granted",
  "partial",
  "전부인정",
  "일부인정",
  "인용",
  "일부시정",
  "전부시정",
]);

const DIRECT_USER_WIN = new Set([
  "dismissed",
  "rejected",
  "기각",
  "각하",
]);

const REHEARING_RESULTS = new Set([
  "upheld",
  "overturned",
  "초심유지",
  "초심취소",
  "초심일부취소",
]);

const WORKER_WIN_PATTERNS = [
  /부당하다/g,
  /양정이\s*과하/g,
  /합리적\s*이유가\s*없/g,
  /부당한/g,
  /위반에\s*해당/g,
  /부당하므로/g,
];

const USER_WIN_PATTERNS = [
  /정당하다/g,
  /하자가\s*없/g,
  /존재하지\s*않/g,
  /적격이\s*없/g,
  /볼\s*수\s*없/g,
  /이유\s*없다/g,
  /근로자에\s*해당하지\s*않/g,
  /갱신기대권이\s*인정되지\s*않/g,
  /해고가\s*존재하지\s*않/g,
];

const WORKER_WIN_STRONG_PATTERNS = [
  /구제신청을\s*인용/g,
  /부당해고에\s*해당/g,
  /부당징계에\s*해당/g,
  /시정명령을\s*한다/g,
];

const USER_WIN_STRONG_PATTERNS = [
  /구제신청을\s*기각/g,
  /각하한다/g,
  /정당한\s*해고/g,
  /정당한\s*징계/g,
];

function getTailText(text) {
  if (!text) return "";
  const value = String(text).trim();
  if (value.length <= 300) return value;
  return value.slice(-300);
}

function getCombinedEvidenceText(row) {
  const parts = [
    row.holding_summary ? `[summary] ${String(row.holding_summary).trim()}` : "",
    row.key_issue ? `[issue] ${String(row.key_issue).trim()}` : "",
    row.holding_points ? `[tail] ${getTailText(row.holding_points)}` : "",
  ].filter(Boolean);

  return parts.join("\n");
}

function getLikelyFinalSentence(text) {
  const normalized = String(text || "")
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?。])\s+|(?<=다\.)\s+|(?<=다)\s+(?=[가-힣])/)
    .map((line) => line.trim())
    .filter(Boolean);

  if (normalized.length === 0) return "";
  return normalized.slice(-3).join(" ");
}

function getLastMatchIndex(text, patterns) {
  let lastIndex = -1;
  for (const pattern of patterns) {
    for (const match of text.matchAll(pattern)) {
      if (typeof match.index === "number" && match.index > lastIndex) {
        lastIndex = match.index;
      }
    }
  }
  return lastIndex;
}

function mapDecisionResult(decisionResult, row) {
  if (DIRECT_WORKER_WIN.has(decisionResult)) {
    return {
      ml_binary_label: "worker_win",
      label_bucket: "인용",
      label_source: decisionResult === "granted" ? "direct" : "mapped",
      needs_review: false,
      exclusion_reason: null,
    };
  }

  if (DIRECT_USER_WIN.has(decisionResult)) {
    return {
      ml_binary_label: "user_win",
      label_bucket: "기각",
      label_source: decisionResult === "dismissed" ? "direct" : "mapped",
      needs_review: false,
      exclusion_reason: null,
    };
  }

  if (REHEARING_RESULTS.has(decisionResult)) {
    const evidenceText = getCombinedEvidenceText(row);
    const finalSentence = getLikelyFinalSentence(evidenceText);
    const workerStrongLast = getLastMatchIndex(finalSentence, WORKER_WIN_STRONG_PATTERNS);
    const userStrongLast = getLastMatchIndex(finalSentence, USER_WIN_STRONG_PATTERNS);

    if (workerStrongLast === -1 && userStrongLast !== -1) {
      return {
        ml_binary_label: "user_win",
        label_bucket: "기각",
        label_source: "mapped",
        needs_review: false,
        exclusion_reason: null,
      };
    }

    if (userStrongLast === -1 && workerStrongLast !== -1) {
      return {
        ml_binary_label: "worker_win",
        label_bucket: "인용",
        label_source: "mapped",
        needs_review: false,
        exclusion_reason: null,
      };
    }

    const workerLast = getLastMatchIndex(evidenceText, [...WORKER_WIN_STRONG_PATTERNS, ...WORKER_WIN_PATTERNS]);
    const userLast = getLastMatchIndex(evidenceText, [...USER_WIN_STRONG_PATTERNS, ...USER_WIN_PATTERNS]);

    if (workerLast === -1 && userLast === -1) {
      return {
        ml_binary_label: null,
        label_bucket: "판단불가",
        label_source: "deferred_rehearing",
        needs_review: true,
        exclusion_reason: "rehearing_tail_pattern_missing",
      };
    }

    if (workerLast > userLast) {
      return {
        ml_binary_label: "worker_win",
        label_bucket: "인용",
        label_source: "mapped",
        needs_review: false,
        exclusion_reason: null,
      };
    }

    return {
      ml_binary_label: "user_win",
      label_bucket: "기각",
      label_source: "mapped",
      needs_review: false,
      exclusion_reason: null,
    };
  }

  switch (decisionResult) {
    default:
      return {
        ml_binary_label: null,
        label_bucket: "판단불가",
        label_source: "deferred_other",
        needs_review: true,
        exclusion_reason: "special_or_unknown_result",
      };
  }
}

function buildDatasetRow(row) {
  const mapped = mapDecisionResult(row.decision_result, row);

  return {
    id: row.id,
    case_number: row.case_number || null,
    decision_result: row.decision_result || null,
    decision_date: row.decision_date || null,
    department: row.department || null,
    issue_type_primary: row.issue_type_primary || null,
    employment_stage: row.employment_stage || null,
    disposition_type: normalizeArray(row.disposition_type),
    fact_markers: normalizeArray(row.fact_markers),
    legal_focus: normalizeArray(row.legal_focus),
    industry_context: row.industry_context || null,
    holding_summary: row.holding_summary || null,
    key_issue: row.key_issue || null,
    holding_points: row.holding_points || null,
    ...mapped,
  };
}

function initStats() {
  return {
    total: 0,
    usable: 0,
    worker_win: 0,
    user_win: 0,
    undecidable: 0,
    direct: 0,
    mapped: 0,
    deferred_rehearing: 0,
    deferred_other: 0,
    decision_result_counts: {},
  };
}

function tally(stats, row) {
  stats.total += 1;
  const resultKey = row.decision_result || "null";
  stats.decision_result_counts[resultKey] = (stats.decision_result_counts[resultKey] || 0) + 1;

  if (row.ml_binary_label === "worker_win") {
    stats.usable += 1;
    stats.worker_win += 1;
  } else if (row.ml_binary_label === "user_win") {
    stats.usable += 1;
    stats.user_win += 1;
  } else {
    stats.undecidable += 1;
  }

  if (row.label_source === "direct") stats.direct += 1;
  if (row.label_source === "mapped") stats.mapped += 1;
  if (row.label_source === "deferred_rehearing") stats.deferred_rehearing += 1;
  if (row.label_source === "deferred_other") stats.deferred_other += 1;
}

function pct(n, d) {
  if (!d) return "0.0%";
  return `${((n / d) * 100).toFixed(1)}%`;
}

function writeReport(reportPath, stats, sampleRows) {
  ensureDir(reportPath);
  const lines = [
    "# Phase C Label Report",
    "",
    `- total: ${stats.total.toLocaleString()}`,
    `- usable: ${stats.usable.toLocaleString()}`,
    `- worker_win: ${stats.worker_win.toLocaleString()} (${pct(stats.worker_win, stats.usable)})`,
    `- user_win: ${stats.user_win.toLocaleString()} (${pct(stats.user_win, stats.usable)})`,
    `- undecidable: ${stats.undecidable.toLocaleString()} (${pct(stats.undecidable, stats.total)})`,
    "",
    "## Label Source",
    "",
    `- direct: ${stats.direct.toLocaleString()}`,
    `- mapped: ${stats.mapped.toLocaleString()}`,
    `- deferred_rehearing: ${stats.deferred_rehearing.toLocaleString()}`,
    `- deferred_other: ${stats.deferred_other.toLocaleString()}`,
    "",
    "## decision_result counts",
    "",
    ...Object.entries(stats.decision_result_counts)
      .sort((a, b) => b[1] - a[1])
      .map(([key, value]) => `- ${key}: ${value.toLocaleString()}`),
    "",
    "## sample rows",
    "",
    ...sampleRows.map(
      (row) =>
        `- ${row.id} | ${row.decision_result} -> ${row.ml_binary_label || row.label_bucket} | ${row.issue_type_primary || "null"}`
    ),
    "",
  ];

  fs.writeFileSync(reportPath, lines.join("\n"), "utf8");
}

async function fetchBatch(from, to) {
  const { data, error } = await supabase
    .from("nlrc_decisions")
    .select(
      "id, case_number, decision_result, decision_date, department, issue_type_primary, employment_stage, disposition_type, fact_markers, legal_focus, industry_context, holding_summary, holding_points"
      + ", key_issue"
    )
    .order("id")
    .range(from, to);

  if (error) {
    throw error;
  }

  return data || [];
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const stats = initStats();
  const sampleRows = [];
  const outputRows = [];

  let from = 0;

  while (true) {
    const batch = await fetchBatch(from, from + PAGE_SIZE - 1);
    if (!batch.length) break;

    for (const row of batch) {
      const datasetRow = buildDatasetRow(row);
      tally(stats, datasetRow);

      if (sampleRows.length < 12) {
        sampleRows.push(datasetRow);
      }

      if (!args.dryRun) {
        outputRows.push(JSON.stringify(datasetRow));
      }

      if (args.limit && stats.total >= args.limit) {
        break;
      }
    }

    if (args.limit && stats.total >= args.limit) {
      break;
    }

    if (batch.length < PAGE_SIZE) break;
    from += PAGE_SIZE;
  }

  if (!args.dryRun) {
    ensureDir(args.output);
    fs.writeFileSync(args.output, `${outputRows.join("\n")}\n`, "utf8");
  }

  writeReport(args.report, stats, sampleRows);

  console.log(JSON.stringify({
    dryRun: args.dryRun,
    total: stats.total,
    usable: stats.usable,
    worker_win: stats.worker_win,
    user_win: stats.user_win,
    undecidable: stats.undecidable,
    output: args.dryRun ? null : args.output,
    report: args.report,
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
