#!/usr/bin/env node
/**
 * Phase C 라벨 데이터셋 정합성 검증기
 *
 * 사용:
 *   node scripts/validate-phase-c-labels.js --input retagging/evaluation/phase_c_labels_v1.jsonl
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

function parseArgs(argv) {
  const args = {
    input: path.join(ROOT, "retagging", "evaluation", "phase_c_labels_v1.jsonl"),
    report: path.join(ROOT, "retagging", "evaluation", "phase_c_label_validation.md"),
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--input") {
      args.input = path.resolve(argv[i + 1]);
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

function expectedLabel(decisionResult) {
  switch (decisionResult) {
    case "granted":
    case "partial":
      return "worker_win";
    case "dismissed":
    case "rejected":
      return "user_win";
    default:
      return null;
  }
}

function validateRow(row) {
  const problems = [];
  const expected = expectedLabel(row.decision_result);

  if (row.ml_binary_label !== "worker_win" && row.ml_binary_label !== "user_win" && row.ml_binary_label !== null) {
    problems.push("invalid_ml_binary_label");
  }

  if (!["인용", "기각", "판단불가"].includes(row.label_bucket)) {
    problems.push("invalid_label_bucket");
  }

  if (
    !["direct", "mapped", "deferred_rehearing", "deferred_other"].includes(row.label_source)
  ) {
    problems.push("invalid_label_source");
  }

  if (expected && row.ml_binary_label && expected !== row.ml_binary_label) {
    problems.push("decision_result_label_mismatch");
  }

  if (!expected && row.ml_binary_label !== null && row.needs_review !== false) {
    problems.push("undecidable_but_labeled_without_clear_rule");
  }

  if (row.ml_binary_label === null && row.needs_review !== true) {
    problems.push("null_label_without_review_flag");
  }

  if (row.ml_binary_label !== null && row.needs_review === true && !row.exclusion_reason) {
    problems.push("labeled_row_marked_review_without_reason");
  }

  return problems;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!fs.existsSync(args.input)) {
    console.error(`Input not found: ${args.input}`);
    process.exit(1);
  }

  const lines = fs.readFileSync(args.input, "utf8").split(/\r?\n/).filter(Boolean);
  const stats = {
    total: 0,
    worker_win: 0,
    user_win: 0,
    undecidable: 0,
    badRows: 0,
  };
  const problemCounts = {};
  const samples = [];

  for (const line of lines) {
    const row = JSON.parse(line);
    stats.total += 1;
    if (row.ml_binary_label === "worker_win") stats.worker_win += 1;
    else if (row.ml_binary_label === "user_win") stats.user_win += 1;
    else stats.undecidable += 1;

    const problems = validateRow(row);
    if (problems.length > 0) {
      stats.badRows += 1;
      for (const problem of problems) {
        problemCounts[problem] = (problemCounts[problem] || 0) + 1;
      }
      if (samples.length < 15) {
        samples.push({
          id: row.id,
          decision_result: row.decision_result,
          ml_binary_label: row.ml_binary_label,
          label_source: row.label_source,
          problems,
        });
      }
    }
  }

  ensureDir(args.report);
  const report = [
    "# Phase C Label Validation",
    "",
    `- total: ${stats.total.toLocaleString()}`,
    `- worker_win: ${stats.worker_win.toLocaleString()}`,
    `- user_win: ${stats.user_win.toLocaleString()}`,
    `- undecidable: ${stats.undecidable.toLocaleString()}`,
    `- bad_rows: ${stats.badRows.toLocaleString()}`,
    "",
    "## problem counts",
    "",
    ...Object.entries(problemCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([key, value]) => `- ${key}: ${value.toLocaleString()}`),
    "",
    "## sample problems",
    "",
    ...samples.map(
      (row) =>
        `- ${row.id} | ${row.decision_result} | ${row.ml_binary_label} | ${row.label_source} | ${row.problems.join(", ")}`
    ),
    "",
  ].join("\n");

  fs.writeFileSync(args.report, report, "utf8");
  console.log(
    JSON.stringify(
      {
        input: args.input,
        report: args.report,
        ...stats,
        problemCounts,
      },
      null,
      2
    )
  );
}

main();
