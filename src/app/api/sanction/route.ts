import { NextRequest, NextResponse } from 'next/server';
import { bucketDecisionResult } from '@/lib/ai/decision-bucket';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { buildComparisonMeta, buildUserContext, splitIssueSummary, trimHistory, type ComparisonCase, type ComparisonMeta } from '@/lib/ai/prompt';
import { SYSTEM_PROMPT } from '@/lib/ai/prompt';

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';
const MAX_MESSAGES = 20;
const MAX_MESSAGE_LENGTH = 4000;
const MAX_TOTAL_CHARS = 16000;

interface StructuredAiCase {
  title: string
  result: string
  key_point: string
}

interface StructuredAiResponse {
  issue_summary: string
  similar_cases: StructuredAiCase[]
  core_differences: string[]
  checklist: string[]
  decision_guide: string[]
  plain_text: string
}

function sanitizeAnalysis(text: string): string {
  const cleaned = text
    .replace(/([0-9]+(\.[0-9]+)?%\s*)(확률|가능성|점수)/gi, '$3')
    .replace(/(승소|패소|인용|기각|정당).{0,12}(확률|가능성 점수)/gi, '$1 판단')
    .replace(/\b(confidence|score)\b/gi, '')
    .replace(/적중률/gi, '판단 근거')
    .replace(/[ \t]{2,}/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return cleaned || text.trim();
}

function extractJsonPayload(text: string): string {
  const trimmed = text.trim();
  if (trimmed.startsWith('{') && trimmed.endsWith('}')) return trimmed;

  const fenced = trimmed.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
  if (fenced?.[1]) return fenced[1].trim();

  const firstBrace = trimmed.indexOf('{');
  const lastBrace = trimmed.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
    return trimmed.slice(firstBrace, lastBrace + 1).trim();
  }

  return trimmed;
}

function parseStructuredAiResponse(text: string): StructuredAiResponse | null {
  try {
    const payload = JSON.parse(extractJsonPayload(text)) as Partial<StructuredAiResponse>;
    if (
      typeof payload.issue_summary !== 'string' ||
      !Array.isArray(payload.similar_cases) ||
      !Array.isArray(payload.core_differences) ||
      !Array.isArray(payload.checklist) ||
      !Array.isArray(payload.decision_guide) ||
      typeof payload.plain_text !== 'string'
    ) {
      return null;
    }

    return {
      issue_summary: payload.issue_summary.trim(),
      similar_cases: payload.similar_cases
        .filter((item): item is StructuredAiCase => !!item && typeof item.title === 'string' && typeof item.result === 'string' && typeof item.key_point === 'string')
        .map((item) => ({
          title: item.title.trim(),
          result: item.result.trim(),
          key_point: item.key_point.trim(),
        })),
      core_differences: payload.core_differences.filter((item): item is string => typeof item === 'string').map((item) => item.trim()).filter(Boolean),
      checklist: payload.checklist.filter((item): item is string => typeof item === 'string').map((item) => item.trim()).filter(Boolean),
      decision_guide: payload.decision_guide.filter((item): item is string => typeof item === 'string').map((item) => item.trim()).filter(Boolean),
      plain_text: payload.plain_text.trim(),
    };
  } catch {
    return null;
  }
}

function normalizeStructuredResult(result: string): string {
  const map: Record<string, string> = {
    '인용': 'granted',
    '기각': 'dismissed',
    '일부인정': 'partial',
    '전부인정': 'granted',
    '각하': 'rejected',
  };
  return map[result.trim()] || result;
}

function textOverlap(a: string, b: string): number {
  if (!a || !b) return 0;
  const wordsA = a.replace(/[○\s]+/g, ' ').trim().split(/\s+/).filter(w => w.length >= 2);
  const wordsB = new Set(b.replace(/[○\s]+/g, ' ').trim().split(/\s+/).filter(w => w.length >= 2));
  if (wordsA.length === 0) return 0;
  const hits = wordsA.filter(w => wordsB.has(w)).length;
  return hits / wordsA.length;
}

function matchSimilarCase(aiCase: StructuredAiCase, pool: Array<Record<string, unknown>>) {
  // 1차: key_point 텍스트로 holding_points와 매칭 (가장 정확)
  const keyPoint = aiCase.key_point || '';
  const resultNorm = normalizeStructuredResult(aiCase.result);

  let bestMatch: Record<string, unknown> | undefined;
  let bestScore = 0;

  for (const candidate of pool) {
    const holding = String(candidate.holding_points || '');
    const summary = String(candidate.summary_short || '');
    const haystack = `${holding} ${summary}`;

    // key_point의 핵심 단어가 holding_points에 포함되는지
    const overlap = textOverlap(keyPoint, haystack);

    // 승패 결과 일치 시 보너스
    const resultMatch = String(candidate.decision_result || '') === resultNorm ? 0.15 : 0;
    const score = overlap + resultMatch;

    if (score > bestScore) {
      bestScore = score;
      bestMatch = candidate;
    }
  }

  // 최소 30% 이상 겹쳐야 매칭 인정
  return bestScore >= 0.3 ? bestMatch : undefined;
}

function buildComparisonFromStructured(
  structured: StructuredAiResponse,
  pool: Array<Record<string, unknown>>,
  dbComparison: ComparisonMeta,
): ComparisonMeta {
  const usedIds = new Set<string>();
  const normalizedCases: ComparisonCase[] = structured.similar_cases.map((item, index) => {
    // 이미 사용된 DB 케이스 제외하고 매칭
    const availablePool = pool.filter(c => !usedIds.has(String(c.id || '')));
    const matched = matchSimilarCase(item, availablePool);

    if (matched) usedIds.add(String(matched.id || ''));

    const decisionResult = matched ? String(matched.decision_result || normalizeStructuredResult(item.result)) : normalizeStructuredResult(item.result);

    const caseId = matched ? String(matched.id || `ai_case_${index}`) : `ai_case_${index}`;
    return {
      id: caseId,
      title: matched ? String(matched.title || item.title) : item.title,
      decision_result: decisionResult,
      holding_points: item.key_point,
      url: matched ? String(matched.url || '') : '',
      summary_short: matched ? String(matched.summary_short || '').slice(0, 160) : item.key_point,
      key_issue: matched ? String(matched.key_issue || '') : '',
      bucket: bucketDecisionResult(decisionResult),
      source: caseId.startsWith('bc_') ? 'court' as const : 'nlrc' as const,
    };
  });

  // 매칭된 real case가 하나도 없으면 DB comparison을 사용
  const hasRealCases = normalizedCases.some(c => !c.id.startsWith('ai_case_'));
  if (!hasRealCases) {
    return {
      ...dbComparison,
      issueSummary: splitIssueSummary(structured.issue_summary),
      coreDifferences: structured.core_differences.length > 0 ? structured.core_differences.slice(0, 4) : dbComparison.coreDifferences,
      checklist: structured.checklist.length > 0 ? structured.checklist.slice(0, 5) : dbComparison.checklist,
      decisionGuide: structured.decision_guide.length > 0 ? structured.decision_guide.slice(0, 4) : dbComparison.decisionGuide,
    };
  }

  return {
    issueSummary: splitIssueSummary(structured.issue_summary),
    workerWinCases: normalizedCases.filter((item) => item.bucket === 'worker_win').slice(0, 2),
    employerWinCases: normalizedCases.filter((item) => item.bucket === 'employer_win').slice(0, 2),
    coreDifferences: structured.core_differences.slice(0, 4),
    checklist: structured.checklist.slice(0, 5),
    decisionGuide: structured.decision_guide.slice(0, 4),
  };
}

function validateMessages(messages: unknown): { valid: true; messages: { role: string; content: string }[] } | { valid: false; error: string } {
  if (!Array.isArray(messages)) {
    return { valid: false, error: 'messages 배열 형식이 올바르지 않습니다.' };
  }

  if (messages.length === 0 || messages.length > MAX_MESSAGES) {
    return { valid: false, error: `messages는 1개 이상 ${MAX_MESSAGES}개 이하만 허용됩니다.` };
  }

  const normalized = messages.map((message) => ({
    role: typeof message?.role === 'string' ? message.role : '',
    content: typeof message?.content === 'string' ? message.content.trim() : '',
  }));

  if (normalized.some((message) => !message.role || !message.content || message.content.length > MAX_MESSAGE_LENGTH)) {
    return { valid: false, error: `각 메시지는 role/content를 가져야 하며, content는 ${MAX_MESSAGE_LENGTH}자 이하여야 합니다.` };
  }

  const totalChars = normalized.reduce((sum, message) => sum + message.content.length, 0);
  if (totalChars > MAX_TOTAL_CHARS) {
    return { valid: false, error: `총 입력 길이는 ${MAX_TOTAL_CHARS}자를 넘길 수 없습니다.` };
  }

  return { valid: true, messages: normalized };
}

export async function POST(req: NextRequest) {
  try {
    if (!ANTHROPIC_API_KEY) {
      return NextResponse.json({ content: 'ANTHROPIC_API_KEY가 설정되지 않았습니다.', tags: [], cases: [] });
    }

    const body = await req.json();
    const validation = validateMessages(body?.messages);
    if (!validation.valid) {
      return NextResponse.json({ content: validation.error, tags: [], cases: [], comparison: null }, { status: 400 });
    }

    const { messages } = validation;
    const lastUserMsg = [...messages].reverse().find((m) => m.role === 'user');
    if (!lastUserMsg) {
      return NextResponse.json({ content: '질문을 입력해주세요.', tags: [], cases: [], comparison: null }, { status: 400 });
    }

    // Step 1: 키워드 추출 (~1ms)
    const tags = extractTags(lastUserMsg.content);

    // Step 2: DB 검색
    const retrieval = await searchCases(tags, lastUserMsg.content);
    const comparison = buildComparisonMeta(lastUserMsg.content, tags, retrieval.cases);

    // Step 3: 프롬프트 조립 + 히스토리 트리밍
    const userContext = buildUserContext(lastUserMsg.content, tags, retrieval.cases);
    const trimmedMessages = trimHistory(messages, userContext);

    // Step 4: Anthropic Haiku 호출 (blocking)
    const resp = await fetch(ANTHROPIC_URL, {
      method: 'POST',
      signal: AbortSignal.timeout(25_000),
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 4096,
        system: SYSTEM_PROMPT,
        messages: trimmedMessages,
        temperature: 0.3,
      }),
    });

    if (!resp.ok) throw new Error(await resp.text());
    const data = await resp.json();
    const rawAnalysis = data.content?.[0]?.text || '분석 결과를 생성할 수 없습니다.';
    const structured = parseStructuredAiResponse(rawAnalysis);
    const analysis = sanitizeAnalysis(structured?.plain_text || rawAnalysis);
    const finalComparison = structured
      ? buildComparisonFromStructured(structured, retrieval.allCases, comparison)
      : comparison;

    return NextResponse.json({
      content: analysis,
      tags: retrieval.tags,
      cases: retrieval.cases,
      comparison: finalComparison,
    });
  } catch (error) {
    const message = error instanceof Error && error.name === 'TimeoutError'
      ? '응답 생성이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.'
      : '일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';

    return NextResponse.json({
      content: message,
      tags: [],
      cases: [],
      comparison: null,
    });
  }
}
