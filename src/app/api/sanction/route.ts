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

// 로컬 키워드 추출 — 42k 판정례 분류에서 검증된 패턴
const KEYWORD_PATTERNS: [RegExp, string][] = [
  // 비위행위 (구체적→일반 순)
  [/횡령|배임|공금|유용|착복|사금고/, '징계해고'],
  [/횡령|배임|공금|유용|착복/, '해고사유'],
  [/폭언|폭행|욕설|폭력|가혹행위|모욕/, '직장내괴롭힘'],
  [/폭언|폭행|욕설|폭력|가혹/, '징계양정'],
  [/성희롱|성추행|성적.*언동|성폭력/, '성희롱'],
  [/무단결근|결근|지각|조퇴|태만|근무태만|직무유기/, '해고사유'],
  [/무단결근|결근|지각|태만/, '징계양정'],
  [/업무능력|성과.*부족|업무.*부적격|근무.*불량|업무.*미숙/, '해고사유'],
  [/기밀|유출|정보.*유출|영업비밀|보안/, '징계해고'],
  [/음주|음주운전|만취/, '징계해고'],
  [/허위|위조|변조|사문서/, '해고사유'],
  [/반말|고객.*민원|불친절|고객.*불만/, '징계양정'],
  [/개인.*용도|사적.*사용|사적.*이용|회사.*차량/, '해고사유'],
  [/겸직|이중.*취업|부업/, '해고사유'],
  [/지시.*불이행|명령.*불복|업무.*거부|업무.*지시/, '해고사유'],
  [/금품.*수수|뇌물|리베이트/, '징계해고'],

  // 사건유형
  [/해고|면직|파면|퇴직.*처리/, '부당해고'],
  [/징계|견책|경고|감봉|정직/, '부당징계'],
  [/전보|전직|배치.*전환|발령/, '전보'],
  [/정직/, '정직'],
  [/감봉/, '감봉'],
  [/수습|시용|수습.*해고/, '수습'],
  [/사직|퇴직|퇴사|합의.*퇴직|권고.*사직/, '사직'],

  // 쟁점
  [/절차.*위반|서면.*통지|해고.*통지|통보.*없이/, '절차위반'],
  [/소명.*기회|의견.*진술|변명.*기회|인사위원회/, '소명기회'],
  [/양정|징계.*수위|과중|비례/, '징계양정'],
  [/갱신.*기대|계약.*갱신|기간제/, '갱신기대권'],
  [/근로자.*지위|근로자.*여부|근로자성/, '근로자성'],

  // 산업
  [/공공기관|공단|공사|재단|진흥원|공기업|지방자치/, '공공기관'],
  [/병원|의료기관|간호|보건|의료법인/, '의료'],
  [/제조|공장|생산.*라인|생산직/, '제조업'],
  [/금융|은행|보험|증권|캐피탈/, '금융'],
  [/학교|대학|교육|학원|교사|교수/, '교육'],
  [/건설|시공|건축|토목/, '건설업'],
  [/운수|버스|택시|화물|운송/, '운수업'],
  [/호텔|음식|유통|마트|서비스/, '서비스업'],
  [/IT|소프트웨어|정보통신|시스템/, 'IT'],
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

const EXTRACT_AND_ANALYZE_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다.

## 작업 1: 키워드 추출
사용자 상황에서 검색 키워드를 추출하세요.
허용 키워드: ${ALL_TAGS.join(', ')}
응답 첫 줄에 JSON 배열로 출력: TAGS:["키워드1","키워드2",...]

## 작업 2: 유사 판정례 기반 분석
제공된 유사 판정례를 참고하여 아래 형식으로 답변:

**예상 징계수위:** (해고/정직/감봉/경고 중 택1, 유사 사례 판정 경향 한 줄)

**필수 절차:**
1. (절차1)
2. (절차2)
3. (절차3)

**주의사항:** (핵심 법적 쟁점 1~2줄)

**참고 조문:** (관련 법 조문)

※ 본 분석은 판정례 통계 기반 참고용이며, 구체적 사안은 노무사와 상담하세요.

규칙:
- 판정례 ID(id_숫자) 노출 금지
- 해시태그(#) 사용 금지
- 공공기관은 징계 유지율이 높은 경향(76.7%) 반영
- 간결하게 답변`;

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
