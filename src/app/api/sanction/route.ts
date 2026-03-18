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

// 로컬 키워드 추출 (GLM 호출 없이 즉시)
const KEYWORD_PATTERNS: [RegExp, string][] = [
  [/횡령|배임|공금/, '징계해고'],
  [/횡령|배임|공금/, '해고사유'],
  [/폭언|폭행|욕설|폭력/, '직장내괴롭힘'],
  [/폭언|폭행|욕설|폭력/, '징계양정'],
  [/성희롱|성적/, '성희롱'],
  [/무단결근|결근|지각|태만/, '해고사유'],
  [/무단결근|결근|지각|태만/, '징계양정'],
  [/업무능력|성과부족|업무부적격/, '해고사유'],
  [/기밀|유출|정보유출/, '징계해고'],
  [/해고/, '부당해고'],
  [/징계/, '부당징계'],
  [/정직/, '정직'],
  [/감봉/, '감봉'],
  [/전보|전직/, '전보'],
  [/수습|시용/, '수습'],
  [/사직|퇴직/, '사직'],
  [/절차|통지|소명/, '절차위반'],
  [/절차|통지|소명/, '소명기회'],
  [/공공기관|공단|공사/, '공공기관'],
  [/병원|의료/, '의료'],
  [/제조|공장/, '제조업'],
  [/금융|은행|보험/, '금융'],
  [/학교|교육/, '교육'],
];

function extractTags(text: string): string[] {
  const tags = new Set<string>();
  for (const [pattern, tag] of KEYWORD_PATTERNS) {
    if (pattern.test(text)) {
      tags.add(tag);
    }
  }
  // 기본 태그 보장
  if (tags.size < 2) {
    tags.add('부당해고');
    tags.add('징계양정');
  }
  return [...tags].filter((t) => (ALL_TAGS as readonly string[]).includes(t));
}

const ANALYSIS_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다. 42,000건의 노동위원회 판정례 통계를 기반으로 징계양정을 분석합니다.

아래 형식으로만 답변하세요:

**예상 징계수위:** (해고/정직/감봉/경고 중 택1, 유사 사례 판정 경향 한 줄)

**필수 절차:**
1. (절차1)
2. (절차2)
3. (절차3)

**주의사항:** (해당 사안의 핵심 법적 쟁점 1~2줄)

**참고 조문:** (관련 법 조문)

※ 본 분석은 판정례 통계 기반 참고용이며, 구체적 사안은 노무사와 상담하세요.

답변 규칙:
- 판정례 ID(id_숫자)를 절대 노출하지 마세요
- 해시태그(#) 사용 금지
- 공공기관은 징계 유지율이 높은 경향(76.7%) 반영
- 300자 이내로 간결하게`;

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

    // Step 1: 로컬 키워드 추출 (즉시, GLM 호출 없음)
    const extractedTags = extractTags(lastUserMsg.content);

    // Step 2: DB 검색 (AND → OR fallback)
    let cases: Record<string, unknown>[] = [];
    const topTags = extractedTags.slice(0, 3);

    const { data: andCases } = await supabase
      .from('nlrc_decisions')
      .select('id, title, decision_result, holding_points, tags, url')
      .contains('tags', topTags)
      .not('holding_points', 'is', null)
      .limit(10);

    if (andCases && andCases.length >= 3) {
      cases = andCases;
    } else {
      const { data: orCases } = await supabase
        .from('nlrc_decisions')
        .select('id, title, decision_result, holding_points, tags, url')
        .overlaps('tags', extractedTags)
        .not('holding_points', 'is', null)
        .limit(10);
      cases = orCases || [];
    }

    // Step 3: GLM 종합 분석 (1회만 호출)
    const caseSummary = cases
      .slice(0, 5)
      .map((c) => `- [${c.id}] ${c.title} [${c.decision_result}]: ${(c.holding_points as string || '').slice(0, 200)}`)
      .join('\n');

    const userContext = `사용자 상황: ${lastUserMsg.content}\n\n추출 키워드: ${extractedTags.join(', ')}\n\n유사 판정례 ${cases.length}건:\n${caseSummary}`;

    const resp = await fetch(GLM_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${GLM_API_KEY}`,
      },
      body: JSON.stringify({
        model: GLM_MODEL,
        messages: [
          { role: 'system', content: ANALYSIS_PROMPT },
          { role: 'user', content: userContext },
        ],
        max_tokens: 4096,
        temperature: 0.3,
      }),
    });

    if (!resp.ok) throw new Error(await resp.text());
    const data = await resp.json();
    const analysis = data.choices?.[0]?.message?.content || '분석 결과를 생성할 수 없습니다.';

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
