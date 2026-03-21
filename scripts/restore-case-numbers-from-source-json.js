#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

const ROOT = path.resolve(__dirname, "..");
const SOURCE_JSON_PATH = "C:\\Users\\iceam\\OneDrive\\5.산업안전\\문서\\Obsidian Vault\\레퍼런스\\최영우\\법제처_노동위결정문_전문.json";
const LOG_DIR = path.join(__dirname, "logs");
const PROGRESS_LOG = path.join(LOG_DIR, "restore-case-number-progress.log");
const FAILURE_LOG = path.join(LOG_DIR, "restore-case-number-failures.jsonl");

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function appendLog(filePath, line) {
  ensureDir(path.dirname(filePath));
  fs.appendFileSync(filePath, `${line}\n`, "utf8");
}

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, "utf8");
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const eq = line.indexOf("=");
    if (eq === -1) continue;
    const key = line.slice(0, eq).trim();
    let value = line.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) process.env[key] = value;
  }
}

function initEnv() {
  try {
    require("dotenv").config({ path: path.join(ROOT, ".env.local") });
    require("dotenv").config({ path: path.join(ROOT, ".env") });
  } catch {
    loadEnvFile(path.join(ROOT, ".env.local"));
    loadEnvFile(path.join(ROOT, ".env"));
  }
}

function parseArgs(argv) {
  const args = {
    dryRun: false,
    limit: 10,
    batchSize: 200,
    source: SOURCE_JSON_PATH,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--dry-run") args.dryRun = true;
    if (token === "--limit" && argv[i + 1]) args.limit = Number(argv[++i]);
    if (token === "--batch-size" && argv[i + 1]) args.batchSize = Number(argv[++i]);
    if (token === "--source" && argv[i + 1]) args.source = argv[++i];
  }

  return args;
}

function getSupabase({ dryRun }) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = dryRun
    ? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    : process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!url || !key) {
    throw new Error("Supabase env is missing.");
  }

  return createClient(url, key, { auth: { persistSession: false } });
}

function loadSourceMap(sourcePath) {
  const raw = fs.readFileSync(sourcePath, "utf8");
  const parsed = JSON.parse(raw);
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error("Source JSON must be an object keyed by id_xxxxx.");
  }
  return parsed;
}

function loadFailedIds() {
  if (!fs.existsSync(FAILURE_LOG)) return new Set();
  const failedIds = new Set();
  for (const line of fs.readFileSync(FAILURE_LOG, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    try {
      const parsed = JSON.parse(line);
      if (parsed?.id) failedIds.add(parsed.id);
    } catch {
      // ignore malformed lines
    }
  }
  return failedIds;
}

function getSourceKeyFromRow(row) {
  const url = typeof row.url === "string" ? row.url : "";
  const match = url.match(/[?&]ID=(\d+)/i);
  if (match?.[1]) return `id_${match[1]}`;
  if (typeof row.id === "string" && /^id_\d+$/i.test(row.id)) return row.id;
  return "";
}

function extractCaseNumber(entry) {
  return String(entry?.["사건번호"] || entry?.caseNumber || "").trim();
}

async function fetchCandidateRows(supabase, desiredCount, skipIds = new Set()) {
  const rows = [];
  const pageSize = Math.min(1000, Math.max(desiredCount * 2, 500));
  let from = 0;

  while (rows.length < desiredCount) {
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("id, url, case_number")
      .order("id", { ascending: true })
      .range(from, from + pageSize - 1);

    if (error) throw error;
    if (!data || data.length === 0) break;

    for (const row of data) {
      if (typeof row.case_number === "string" && /^id_/i.test(row.case_number) && !skipIds.has(row.id)) {
        rows.push(row);
        if (rows.length >= desiredCount) break;
      }
    }

    if (data.length < pageSize) break;
    from += pageSize;
  }

  return rows;
}

async function updateCaseNumber(supabase, id, caseNumber) {
  const { error } = await supabase
    .from("nlrc_decisions")
    .update({ case_number: caseNumber })
    .eq("id", id);
  if (error) throw error;
}

async function countIdCaseNumbers(supabase) {
  let count = 0;
  const pageSize = 1000;
  let from = 0;

  while (true) {
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("case_number")
      .order("id", { ascending: true })
      .range(from, from + pageSize - 1);
    if (error) throw error;
    if (!data || data.length === 0) break;

    for (const row of data) {
      if (typeof row.case_number === "string" && /^id_/i.test(row.case_number)) {
        count += 1;
      }
    }

    if (data.length < pageSize) break;
    from += pageSize;
  }

  return count;
}

async function main() {
  initEnv();
  ensureDir(LOG_DIR);

  const args = parseArgs(process.argv.slice(2));
  const targetCount = args.dryRun ? args.limit : args.batchSize;
  const supabase = getSupabase({ dryRun: args.dryRun });
  const sourceMap = loadSourceMap(args.source);
  const failedIds = loadFailedIds();

  appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] start dryRun=${args.dryRun} target=${targetCount}`);

  let processed = 0;
  let batchIndex = 0;

  while (true) {
    const rows = await fetchCandidateRows(supabase, targetCount, failedIds);
    if (rows.length === 0) break;

    batchIndex += 1;
    console.log(`Loaded ${rows.length} id_* case_number rows from DB (batch ${batchIndex}).`);

    for (const row of rows) {
      try {
        const sourceKey = getSourceKeyFromRow(row);
        const entry = sourceMap[sourceKey];
        if (!entry) {
          throw new Error("Missing source JSON entry");
        }

        const caseNumber = extractCaseNumber(entry);
        if (!caseNumber || /^id_/i.test(caseNumber)) {
          throw new Error("Source JSON case_number is missing or invalid");
        }

        if (args.dryRun) {
          console.log(`\n[DRY-RUN] ${row.id}`);
          console.log(`source_key: ${sourceKey || "(none)"}`);
          console.log(`db_case_number: ${row.case_number || "(none)"}`);
          console.log(`source_case_number: ${caseNumber}`);
        } else {
          await updateCaseNumber(supabase, row.id, caseNumber);
          appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] updated ${row.id} case_number=${caseNumber}`);
        }

        processed += 1;
        if (!args.dryRun && processed % 500 === 0) {
          appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] checkpoint processed=${processed}`);
          console.log(`Checkpoint: processed=${processed}`);
        }
      } catch (error) {
        failedIds.add(row.id);
        appendLog(
          FAILURE_LOG,
          JSON.stringify({
            ts: new Date().toISOString(),
            id: row.id,
            error: error instanceof Error ? error.message : String(error),
          })
        );
        console.error(`Failed ${row.id}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }

    if (args.dryRun) break;
  }

  const remainingIdCount = await countIdCaseNumbers(supabase);
  appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] done processed=${processed} remaining_id_case_number=${remainingIdCount}`);
  console.log(`Done. processed=${processed}, dryRun=${args.dryRun}, remainingIdCaseNumber=${remainingIdCount}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
