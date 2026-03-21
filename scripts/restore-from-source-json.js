#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

const ROOT = path.resolve(__dirname, "..");
const SOURCE_JSON_PATH = "C:\\Users\\iceam\\OneDrive\\5.산업안전\\문서\\Obsidian Vault\\레퍼런스\\최영우\\법제처_노동위결정문_전문.json";
const LOG_DIR = path.join(__dirname, "logs");
const PROGRESS_LOG = path.join(LOG_DIR, "restore-from-source-progress.log");
const FAILURE_LOG = path.join(LOG_DIR, "restore-from-source-failures.jsonl");
const loadedEnvState = {
  fileAnonKey: "",
  fileServiceRoleKey: "",
};

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function appendLog(filePath, line) {
  ensureDir(path.dirname(filePath));
  fs.appendFileSync(filePath, `${line}\n`, "utf8");
}

function parseArgs(argv) {
  const args = {
    dryRun: false,
    limit: 10,
    batchSize: 50,
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
    const localResult = require("dotenv").config({ path: path.join(ROOT, ".env.local") });
    const envResult = require("dotenv").config({ path: path.join(ROOT, ".env") });
    loadedEnvState.fileAnonKey =
      localResult?.parsed?.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
      envResult?.parsed?.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
      "";
    loadedEnvState.fileServiceRoleKey =
      localResult?.parsed?.SUPABASE_SERVICE_ROLE_KEY ||
      envResult?.parsed?.SUPABASE_SERVICE_ROLE_KEY ||
      "";
  } catch {
    loadEnvFile(path.join(ROOT, ".env.local"));
    loadEnvFile(path.join(ROOT, ".env"));
    loadedEnvState.fileAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";
    loadedEnvState.fileServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || "";
  }
}

function getSupabase({ dryRun }) {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = dryRun
    ? loadedEnvState.fileAnonKey || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    : loadedEnvState.fileServiceRoleKey ||
      process.env.SUPABASE_SERVICE_ROLE_KEY ||
      loadedEnvState.fileAnonKey ||
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !key) {
    throw new Error("Supabase env is missing.");
  }

  return createClient(url, key, { auth: { persistSession: false } });
}

function cleanHtml(input) {
  if (!input) return "";
  return String(input)
    .replace(/<\s*br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n")
    .replace(/<p[^>]*>/gi, "")
    .replace(/<\/div>/gi, "\n")
    .replace(/<div[^>]*>/gi, "")
    .replace(/<\/li>/gi, "\n")
    .replace(/<li[^>]*>/gi, "· ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/<[^>]+>/g, " ")
    .replace(/\r/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
}

function getCandidateText(entry) {
  const holdingYoji = cleanHtml(entry["판정요지"]);
  const holdingSahang = cleanHtml(entry["판정사항"]);
  const content = cleanHtml(entry["내용"]);
  return {
    holdingPoints: holdingYoji || content,
    holdingSummary: holdingSahang || "",
    caseNumber:
      String(
        entry["사건번호"] ||
        entry.caseNumber ||
        ""
      ).trim(),
  };
}

function getSourceKeyFromRow(row) {
  const url = typeof row.url === "string" ? row.url : "";
  const match = url.match(/[?&]ID=(\d+)/i);
  if (match?.[1]) return `id_${match[1]}`;
  if (typeof row.id === "string" && /^id_\d+$/i.test(row.id)) return row.id;
  return "";
}

function loadSourceMap(sourcePath) {
  const raw = fs.readFileSync(sourcePath, "utf8");
  const parsed = JSON.parse(raw);
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error("Source JSON must be an object keyed by id_xxxxx.");
  }
  return parsed;
}

async function fetchCandidateRows(supabase, desiredCount) {
  const { data, error } = await supabase
    .from("nlrc_decisions")
    .select("id, url, holding_points, case_number")
    .order("id", { ascending: true })
    .limit(Math.max(desiredCount * 5, 200));

  if (error) throw error;

  return (data || []).filter((row) => {
    const length = typeof row.holding_points === "string" ? row.holding_points.trim().length : 0;
    return length < 100;
  }).slice(0, desiredCount);
}

async function updateDecisionRecord(supabase, id, holdingPoints, holdingSummary, caseNumber) {
  const payload = { holding_points: holdingPoints };
  if (holdingSummary) payload.holding_summary = holdingSummary;
  if (caseNumber && !/^id_/i.test(caseNumber)) payload.case_number = caseNumber;

  const { error } = await supabase.from("nlrc_decisions").update(payload).eq("id", id);
  if (error) throw error;
}

async function main() {
  initEnv();
  ensureDir(LOG_DIR);

  const args = parseArgs(process.argv.slice(2));
  const targetCount = args.dryRun ? args.limit : args.batchSize;
  const supabase = getSupabase({ dryRun: args.dryRun });
  const sourceMap = loadSourceMap(args.source);

  appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] start dryRun=${args.dryRun} target=${targetCount}`);

  const rows = await fetchCandidateRows(supabase, targetCount);
  console.log(`Loaded ${rows.length} short holding_points rows from DB.`);

  let processed = 0;
  for (const row of rows) {
    try {
      const sourceEntry = sourceMap[row.id];
      const sourceKey = getSourceKeyFromRow(row);
      const resolvedEntry = sourceMap[sourceKey];
      if (!resolvedEntry) {
        throw new Error("Missing source JSON entry");
      }

      const { holdingPoints, holdingSummary, caseNumber } = getCandidateText(resolvedEntry);
      if (!holdingPoints || holdingPoints.length < 100) {
        throw new Error("Source JSON holding text is too short or missing");
      }

      if (args.dryRun) {
        console.log(`\n[DRY-RUN] ${row.id}`);
        console.log(`source_key: ${sourceKey || "(none)"}`);
        console.log(`case_number: ${caseNumber || row.case_number || "(none)"}`);
        console.log(`holding_points.length=${holdingPoints.length}`);
        console.log(`holding_summary.length=${holdingSummary.length}`);
        console.log(holdingPoints.slice(0, 600));
      } else {
        await updateDecisionRecord(supabase, row.id, holdingPoints, holdingSummary, caseNumber);
        appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] updated ${row.id} len=${holdingPoints.length}`);
      }

      processed += 1;
    } catch (error) {
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

  appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] done processed=${processed}`);
  console.log(`Done. processed=${processed}, dryRun=${args.dryRun}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
