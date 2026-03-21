#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { createClient } = require("@supabase/supabase-js");

const ROOT = path.resolve(__dirname, "..");
const LOG_DIR = path.join(__dirname, "logs");
const PROGRESS_LOG = path.join(LOG_DIR, "restore-progress.log");
const FAILURE_LOG = path.join(LOG_DIR, "restore-failures.jsonl");
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
    delayMs: 1000,
    scanChunk: 500,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--dry-run") args.dryRun = true;
    if (token === "--limit" && argv[i + 1]) args.limit = Number(argv[++i]);
    if (token === "--batch-size" && argv[i + 1]) args.batchSize = Number(argv[++i]);
    if (token === "--delay-ms" && argv[i + 1]) args.delayMs = Number(argv[++i]);
    if (token === "--scan-chunk" && argv[i + 1]) args.scanChunk = Number(argv[++i]);
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
    throw new Error("Supabase env is missing. Check NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY/NEXT_PUBLIC_SUPABASE_ANON_KEY.");
  }

  return createClient(url, key, { auth: { persistSession: false } });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function decodeHtmlEntities(text) {
  return text
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'");
}

function stripHtml(html) {
  return decodeHtmlEntities(
    html
      .replace(/<\s*br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n")
      .replace(/<\/div>/gi, "\n")
      .replace(/<\/li>/gi, "\n")
      .replace(/<li[^>]*>/gi, "· ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\r/g, "")
      .replace(/[ \t]+\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .replace(/[ \t]{2,}/g, " ")
      .trim()
  );
}

function extractCaseNumberFromText(text) {
  const patterns = [
    /\[\s*(\d{4}[가-힣]+\d+[가-힣]*)\s*,/u,
    /사건번호\s*[:：]\s*([^\n]+)/u,
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]) {
      return match[1].trim();
    }
  }
  return "";
}

function extractSectionBetween(text, startLabel, nextLabels) {
  const startIndex = text.indexOf(startLabel);
  if (startIndex === -1) return "";
  const searchStart = startIndex + startLabel.length;
  let endIndex = text.length;
  for (const nextLabel of nextLabels) {
    const idx = text.indexOf(nextLabel, searchStart);
    if (idx !== -1 && idx < endIndex) endIndex = idx;
  }
  return text.slice(searchStart, endIndex).trim();
}

function normalizeHoldingText(text) {
  return text
    .replace(/\u00a0/g, " ")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

async function fetchHoldingFromAPI(url) {
  const response = await fetch(url, {
    redirect: "follow",
    headers: {
      "User-Agent": "labor-decisions-search/restore-holding-points",
      Accept: "text/html,application/xhtml+xml",
    },
  });

  if (!response.ok) {
    throw new Error(`Fetch failed: ${response.status} ${response.statusText}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  let html = Buffer.from(arrayBuffer).toString("utf8");

  if (html.includes("�") || /charset=EUC-KR/i.test(html)) {
    try {
      const decoder = new TextDecoder("euc-kr");
      html = decoder.decode(arrayBuffer);
    } catch {
      // Keep UTF-8 decode fallback when euc-kr decoder is unavailable.
    }
  }

  return html;
}

function parseHoldingSection(html) {
  const text = stripHtml(html);
  const caseNumber = extractCaseNumberFromText(text);

  const holdingYoji =
    extractSectionBetween(text, "【판정요지】", ["【판정결과】", "【결정요지】", "【판정사항】"]) ||
    extractSectionBetween(text, "[판정요지]", ["[판정결과]", "[결정요지]", "[판정사항]"]);

  const decisionYoji =
    extractSectionBetween(text, "【결정요지】", ["【판정사항】", "【판정요지】", "【주문】"]) ||
    extractSectionBetween(text, "[결정요지]", ["[판정사항]", "[판정요지]", "[주문]"]);

  const bestText = normalizeHoldingText(holdingYoji || decisionYoji);
  return { holdingText: bestText, caseNumber };
}

async function updateDecisionRecord(supabase, id, holdingText, caseNumber) {
  const payload = { holding_points: holdingText };
  if (caseNumber && !/^id_/i.test(caseNumber)) {
    payload.case_number = caseNumber;
  }

  const { error } = await supabase.from("nlrc_decisions").update(payload).eq("id", id);
  if (error) throw error;
}

async function fetchCandidateRows(supabase, scanChunk, desiredCount) {
  const collected = [];
  let from = 0;

  while (collected.length < desiredCount) {
    const to = from + scanChunk - 1;
    const { data, error } = await supabase
      .from("nlrc_decisions")
      .select("id, url, holding_points, case_number")
      .order("id", { ascending: true })
      .range(from, to);

    if (error) throw error;
    if (!data || data.length === 0) break;

    for (const row of data) {
      const length = typeof row.holding_points === "string" ? row.holding_points.trim().length : 0;
      if (length < 100) {
        collected.push(row);
        if (collected.length >= desiredCount) break;
      }
    }

    from += scanChunk;
  }

  return collected;
}

async function main() {
  initEnv();
  ensureDir(LOG_DIR);

  const args = parseArgs(process.argv.slice(2));
  const targetCount = args.dryRun ? args.limit : args.batchSize;
  const supabase = getSupabase({ dryRun: args.dryRun });

  appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] start dryRun=${args.dryRun} target=${targetCount}`);

  const rows = await fetchCandidateRows(supabase, args.scanChunk, targetCount);
  console.log(`Loaded ${rows.length} candidate rows (holding_points < 100 chars).`);

  let processed = 0;
  for (const row of rows) {
    const originalLength = typeof row.holding_points === "string" ? row.holding_points.trim().length : 0;
    try {
      if (!row.url) {
        throw new Error("Missing url");
      }

      const html = await fetchHoldingFromAPI(row.url);
      const { holdingText, caseNumber } = parseHoldingSection(html);

      if (!holdingText || holdingText.length < 100) {
        throw new Error("Parsed holding text is too short or missing");
      }

      if (args.dryRun) {
        console.log(`\n[DRY-RUN] ${row.id}`);
        console.log(`case_number: ${caseNumber || row.case_number || "(none)"}`);
        console.log(`before_len=${originalLength}, after_len=${holdingText.length}`);
        console.log(holdingText.slice(0, 600));
      } else {
        await updateDecisionRecord(supabase, row.id, holdingText, caseNumber);
        appendLog(PROGRESS_LOG, `[${new Date().toISOString()}] updated ${row.id} before=${originalLength} after=${holdingText.length}`);
      }

      processed += 1;
      if (!args.dryRun) {
        await sleep(args.delayMs);
      }
    } catch (error) {
      appendLog(
        FAILURE_LOG,
        JSON.stringify({
          ts: new Date().toISOString(),
          id: row.id,
          url: row.url,
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
