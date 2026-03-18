import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { ALL_TAGS } from '@/lib/tags';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const GLM_API_KEY = process.env.GLM_API_KEY;
const GLM_URL = 'https://api.z.ai/api/paas/v4/chat/completions';
const GLM_MODEL = 'GLM-4.7-Flash';

async function callGLM(systemPrompt: string, userMessage: string): Promise<string> {
  const resp = await fetch(GLM_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${GLM_API_KEY}`,
    },
    body: JSON.stringify({
      model: GLM_MODEL,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userMessage },
      ],
      max_tokens: 2048,
      temperature: 0.3,
    }),
  });

  if (!resp.ok) {
    const error = await resp.text();
    throw new Error(`GLM API error: ${error}`);
  }

  const data = await resp.json();
  return data.choices?.[0]?.message?.content || '';
}

const EXTRACT_PROMPT = `당신은 노동법 키워드 추출기입니다. 사용자의 상황 설명에서 관련 키워드를 추출하세요.

허용된 키워드 목록:
${ALL_TAGS.join(', ')}

규칙:
- 위 목록에서만 선택
- 3~7개 키워드
- JSON 배열로만 응답, 설명 없이
- 예: ["징계해고", "해고사유", "절차위반"]`;

const ANALYSIS_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다. 42,000건의 노동위원회 판정례 데이터를 기반으로 징계양정을 분석합니다.

사용자의 상황과 유사 판정례를 바탕으로 다음을 안내하세요:

1. **예상 징계수위**: 유사 사례의 판정 경향 분석 (인용/기각 비율 포함)
2. **필수 절차 체크리스트**: 해당 징계 유형에 필요한 절차 (인사위원회, 소명기회, 서면통지 등)
3. **주의사항**: 해당 사안에서 특별히 주의할 법적 쟁점
4. **근거 판정례**: 인용한 판정례의 사건번호와 핵심 내용

답변 규칙:
- 구조화된 마크다운 형식
- 조문 번호 포함 (근로기준법 제23조 등)
- 공공기관의 경우 징계 유지율이 높은 경향(76.7%)을 반영
- 답변 마지막에 반드시: "※ 본 분석은 노동위 판정례 통계에 기반한 참고용이며, 구체적 사안은 반드시 노무사와 상담하세요."`;

export async function POST(req: NextRequest) {
  try {
    if (!GLM_API_KEY) {
      return NextResponse.json({ content: 'GLM_API_KEY가 설정되지 않았습니다.', tags: [], cases: [] });
    }

    const { messages } = await req.json();
    const lastUserMsg = [...messages].reverse().find((m: { role: string }) => m.role === 'user');
    if (!lastUserMsg) {
      return NextResponse.json({ content: '질문을 입력해주세요.', tags: [], cases: [] });
    }

    // Step 1: 키워드 추출
    const tagResponse = await callGLM(EXTRACT_PROMPT, lastUserMsg.content);
    let extractedTags: string[] = [];
    try {
      const match = tagResponse.match(/\[[\s\S]*?\]/);
      if (match) {
        extractedTags = JSON.parse(match[0]).filter((t: string) => (ALL_TAGS as readonly string[]).includes(t));
      }
    } catch {
      extractedTags = ['부당해고', '징계양정'];
    }

    if (extractedTags.length === 0) {
      extractedTags = ['부당해고', '징계양정'];
    }

    // Step 2: 유사 판정례 검색 (점진적 확장)
    let cases: Record<string, unknown>[] = [];

    // AND 매칭 시도 (상위 3개 태그)
    const topTags = extractedTags.slice(0, 3);
    const { data: andCases } = await supabase
      .from('nlrc_decisions')
      .select('id, title, decision_result, holding_points, tags, url')
      .contains('tags', topTags)
      .limit(10);

    if (andCases && andCases.length >= 3) {
      cases = andCases;
    } else {
      // OR 매칭 fallback
      const { data: orCases } = await supabase
        .from('nlrc_decisions')
        .select('id, title, decision_result, holding_points, tags, url')
        .overlaps('tags', extractedTags)
        .limit(10);
      cases = orCases || [];
    }

    // Step 3: 종합 분석
    const caseSummary = cases
      .slice(0, 5)
      .map((c) => `- [${c.id}] ${c.title} [${c.decision_result}]: ${(c.holding_points as string || '').slice(0, 200)}`)
      .join('\n');

    const userContext = `사용자 상황: ${lastUserMsg.content}\n\n추출된 키워드: ${extractedTags.join(', ')}\n\n유사 판정례 ${cases.length}건:\n${caseSummary}`;

    const analysis = await callGLM(ANALYSIS_PROMPT, userContext);

    return NextResponse.json({
      content: analysis,
      tags: extractedTags,
      cases: cases.slice(0, 5).map((c) => ({
        id: c.id,
        title: c.title,
        decision_result: c.decision_result,
        holding_points: (c.holding_points as string || '').slice(0, 150),
        url: c.url,
      })),
    });
  } catch (error) {
    return NextResponse.json(
      { content: `오류: ${error instanceof Error ? error.message : '알 수 없는 오류'}`, tags: [], cases: [] },
      { status: 200 }
    );
  }
}
