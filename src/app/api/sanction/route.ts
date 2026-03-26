import { NextRequest, NextResponse } from 'next/server';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { buildComparisonMeta, buildUserContext, trimHistory } from '@/lib/ai/prompt';
import { SYSTEM_PROMPT } from '@/lib/ai/prompt';

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';
const MAX_MESSAGES = 20;
const MAX_MESSAGE_LENGTH = 4000;
const MAX_TOTAL_CHARS = 16000;

function sanitizeAnalysis(text: string): string {
  const bannedPatterns = [
    /(승소|패소|인용|기각|정당).{0,12}(확률|가능성 점수)/i,
    /(적중률|confidence|score)/i,
    /[0-9]+(\.[0-9]+)?%\s*(확률|가능성|점수)/i,
  ];

  return text
    .split('\n')
    .filter((line) => !bannedPatterns.some((pattern) => pattern.test(line)))
    .join('\n')
    .trim();
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
    const comparison = buildComparisonMeta(lastUserMsg.content, tags, retrieval.allCases);

    // Step 3: 프롬프트 조립 + 히스토리 트리밍
    const userContext = buildUserContext(lastUserMsg.content, tags, retrieval.allCases);
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
    const analysis = sanitizeAnalysis(rawAnalysis);

    return NextResponse.json({
      content: analysis,
      tags: retrieval.tags,
      cases: retrieval.cases,
      comparison,
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
