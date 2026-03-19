import { NextRequest } from 'next/server';
import { extractTags, searchCases } from '@/lib/ai/retrieval';
import { buildUserContext, trimHistory } from '@/lib/ai/prompt';
import { createStreamingResponse } from '@/lib/ai/stream';

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

export async function POST(req: NextRequest) {
  try {
    if (!ANTHROPIC_API_KEY) {
      return jsonResponse({ content: 'ANTHROPIC_API_KEY가 설정되지 않았습니다.', tags: [], cases: [] });
    }

    const { messages } = await req.json();
    const lastUserMsg = [...messages].reverse().find((m: { role: string }) => m.role === 'user');
    if (!lastUserMsg) {
      return jsonResponse({ content: '질문을 입력해주세요.', tags: [], cases: [] });
    }

    // Step 1: 키워드 추출 (~1ms)
    const tags = extractTags(lastUserMsg.content);

    // Step 2: DB 검색 (AND → OR fallback)
    const retrieval = await searchCases(tags);

    // Step 3: 프롬프트 조립 + 히스토리 트리밍
    const userContext = buildUserContext(lastUserMsg.content, tags, retrieval.allCases);
    const trimmedMessages = trimHistory(messages, userContext);

    // Step 4: 스트리밍 응답
    return createStreamingResponse({
      apiKey: ANTHROPIC_API_KEY,
      messages: trimmedMessages,
      tags: retrieval.tags,
      cases: retrieval.cases,
    });
  } catch (error) {
    return jsonResponse({
      content: `오류가 발생했습니다: ${error instanceof Error ? error.message : '알 수 없는 오류'}. 잠시 후 다시 시도해 주세요.`,
      tags: [],
      cases: [],
    });
  }
}

function jsonResponse(data: { content: string; tags: string[]; cases: unknown[] }) {
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  });
}
