import { NextRequest, NextResponse } from 'next/server';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { buildUserContext, trimHistory } from '@/lib/ai/prompt';
import { SYSTEM_PROMPT } from '@/lib/ai/prompt';

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';

export async function POST(req: NextRequest) {
  try {
    if (!ANTHROPIC_API_KEY) {
      return NextResponse.json({ content: 'ANTHROPIC_API_KEY가 설정되지 않았습니다.', tags: [], cases: [] });
    }

    const { messages } = await req.json();
    const lastUserMsg = [...messages].reverse().find((m: { role: string }) => m.role === 'user');
    if (!lastUserMsg) {
      return NextResponse.json({ content: '질문을 입력해주세요.', tags: [], cases: [] });
    }

    // Step 1: 키워드 추출 (~1ms)
    const tags = extractTags(lastUserMsg.content);

    // Step 2: DB 검색
    const retrieval = await searchCases(tags, lastUserMsg.content);

    // Step 3: 프롬프트 조립 + 히스토리 트리밍
    const userContext = buildUserContext(lastUserMsg.content, tags, retrieval.allCases);
    const trimmedMessages = trimHistory(messages, userContext);

    // Step 4: Anthropic Haiku 호출 (blocking)
    const resp = await fetch(ANTHROPIC_URL, {
      method: 'POST',
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
    const analysis = data.content?.[0]?.text || '분석 결과를 생성할 수 없습니다.';

    return NextResponse.json({
      content: analysis,
      tags: retrieval.tags,
      cases: retrieval.cases,
    });
  } catch (error) {
    return NextResponse.json({
      content: '일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.',
      tags: [],
      cases: [],
    });
  }
}
