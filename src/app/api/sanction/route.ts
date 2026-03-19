import { NextRequest } from 'next/server';
import { createClient } from '@supabase/supabase-js';
import { ALL_TAGS } from '@/lib/tags';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';
const REQUEST_TIMEOUT_MS = 15_000;
const MAX_HISTORY_MESSAGES = 6;

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

const SYSTEM_PROMPT = `당신은 대한민국 노동법 전문 AI 자문입니다. 42,000건의 노동위원회 판정례 데이터베이스를 기반으로 답변합니다.

## 최우선 원칙: 근거 기반 답변 (Retrieve-First)
당신의 모든 분석은 **제공된 유사 판정례**에 근거해야 합니다.
- 판정례가 제공되면: 해당 사례들의 판정 경향을 근거로 분석
- 판정례가 부족하면: "유사 사례가 부족하여 확정적 판단이 어렵습니다"라고 명시
- 판정례가 없으면: 판정례를 찾지 못했다고 안내하고, 노무사 상담을 권장. 일반 법리 설명도 최소화

⚠️ 절대 하지 말 것:
- 제공된 판정례 없이 "일반적으로~", "통상적으로~"라는 식의 확정적 법률 판단
- 판정례에 없는 통계 수치나 확률 언급
- 근거 없는 구체적 징계수위 예측

## 탐침 원칙
사용자의 상황 설명이 불충분하면, 바로 분석하지 말고 먼저 아래 3가지 관점에서 핵심 질문을 하세요:
1. **사유 관점**: 구체적 비위행위, 발생 횟수, 증거 유무
2. **양정 관점**: 근속연수, 과거 징계 이력, 반성 여부, 피해 규모
3. **절차 관점**: 인사위원회 개최 여부, 소명 기회 부여, 서면 통지

충분한 정보가 있다면 바로 분석하되, 빈약한 1~2줄 상황 설명에는 반드시 추가 질문부터 하세요.

## 분석 형식 (충분한 정보 + 유사 판정례가 있을 때)

**쟁점 요약:** (사안의 핵심 쟁점 1~2줄)

**유사 판정례 분석:**
(제공된 판정례 중 관련성 높은 사례의 판정 경향 요약. "제공된 N건의 유사 사례 중~" 형식)

**예상 징계수위:** (해고/정직/감봉/경고 중 택1 + 유사 사례 기반 근거 한 줄)

**필수 절차:**
1. (절차1)
2. (절차2)
3. (절차3)

**주의사항:** (유사 판정례에서 드러난 핵심 법적 쟁점 1~2줄)

**참고 조문:** (관련 법 조문)

※ 본 분석은 판정례 통계 기반 참고용이며, 구체적 사안은 노무사와 상담하세요.

## 근거 부족 시 형식

**쟁점 요약:** (사안의 핵심 쟁점)

**판정례 검색 결과:** 관련 판정례를 충분히 찾지 못했습니다. 현재 확보된 사례만으로는 구체적 판단이 어렵습니다.

**권고:** 정확한 판단을 위해 노무사 상담을 권장합니다.

규칙:
- 판정례 ID(id_숫자) 노출 금지
- 해시태그(#) 사용 금지
- 공공기관은 징계 유지율이 높은 경향(76.7%) 반영
- 간결하게 답변
- "일반적으로", "통상적으로" 등의 표현은 반드시 판정례 근거와 함께만 사용`;

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

    // Step 1: 로컬 키워드 추출 (~1ms)
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

    // 판정례 요약 + 메타데이터
    const topCases = cases.slice(0, 5);
    const caseSummary = topCases
      .map((c) => `- ${c.title} [${c.decision_result}]: ${(c.holding_points as string || '').slice(0, 200)}`)
      .join('\n');

    const caseCards = topCases.map((c) => ({
      id: c.id,
      title: c.title,
      decision_result: c.decision_result,
      holding_points: (c.holding_points as string || '').slice(0, 150),
      url: c.url,
    }));

    // Step 3: 대화 히스토리 트리밍 (최근 MAX_HISTORY_MESSAGES개만)
    const trimmedHistory = messages
      .slice(-MAX_HISTORY_MESSAGES)
      .map((m: { role: string; content: string }) => ({
        role: m.role,
        content: m.content,
      }));

    // 검색 결과 강도에 따른 프롬프트 분기
    let retrievalInstruction: string;
    if (cases.length === 0) {
      retrievalInstruction = '\n\n⚠️ [검색 결과 없음] 유사 판정례를 찾지 못했습니다. "근거 부족 시 형식"으로 답변하세요. 구체적 징계수위 예측이나 판정 경향 언급을 하지 마세요.';
    } else if (cases.length <= 2) {
      retrievalInstruction = '\n\n⚠️ [검색 결과 부족] 유사 판정례가 2건 이하로 충분하지 않습니다. 제공된 사례를 참고하되, "유사 사례가 적어 확정적 판단은 어렵습니다"라고 명시하세요.';
    } else {
      retrievalInstruction = `\n\n✅ [검색 결과 ${cases.length}건] 충분한 유사 판정례가 확보되었습니다. 이 사례들을 근거로 분석하세요.`;
    }
    const userContext = `사용자 상황: ${lastUserMsg.content}\n\n추출 키워드: ${extractedTags.join(', ')}\n\n유사 판정례 ${cases.length}건:\n${caseSummary}${retrievalInstruction}`;
    if (trimmedHistory.length > 0) {
      trimmedHistory[trimmedHistory.length - 1] = { role: 'user', content: userContext };
    }

    // Step 4: Anthropic Haiku 스트리밍 호출
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
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
          messages: trimmedHistory,
          temperature: 0.3,
          stream: true,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Anthropic API ${resp.status}: ${errText.slice(0, 200)}`);
      }

      // SSE 스트리밍 응답 변환
      const encoder = new TextEncoder();
      const stream = new ReadableStream({
        async start(streamController) {
          // 먼저 메타데이터(태그, 판정례) 전송
          streamController.enqueue(
            encoder.encode(`data: ${JSON.stringify({ type: 'meta', tags: extractedTags, cases: caseCards })}\n\n`)
          );

          const reader = resp.body!.getReader();
          const decoder = new TextDecoder();
          let buffer = '';
          let totalChars = 0;

          try {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;

              buffer += decoder.decode(value, { stream: true });
              const lines = buffer.split('\n');
              buffer = lines.pop() || '';

              for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const payload = line.slice(6);
                if (payload === '[DONE]') continue;

                try {
                  const event = JSON.parse(payload);
                  if (event.type === 'content_block_delta' && event.delta?.text) {
                    totalChars += event.delta.text.length;
                    streamController.enqueue(
                      encoder.encode(`data: ${JSON.stringify({ type: 'delta', text: event.delta.text })}\n\n`)
                    );
                  }
                } catch {
                  // 파싱 실패한 청크는 무시
                }
              }
            }

            // 비정상 종료 감지: 텍스트가 거의 없이 스트림이 끝난 경우
            if (totalChars < 10) {
              streamController.enqueue(
                encoder.encode(`data: ${JSON.stringify({ type: 'error', message: '응답이 비정상적으로 종료되었습니다. 다시 시도해 주세요.' })}\n\n`)
              );
            }
            streamController.enqueue(encoder.encode(`data: ${JSON.stringify({ type: 'done' })}\n\n`));
          } catch (err) {
            const errMsg = err instanceof Error ? err.message : 'stream error';
            streamController.enqueue(
              encoder.encode(`data: ${JSON.stringify({ type: 'error', message: errMsg })}\n\n`)
            );
            streamController.enqueue(encoder.encode(`data: ${JSON.stringify({ type: 'done' })}\n\n`));
          } finally {
            streamController.close();
          }
        },
      });

      return new Response(stream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } catch (err) {
      clearTimeout(timeout);

      if (err instanceof DOMException && err.name === 'AbortError') {
        return jsonResponse({
          content: '응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.',
          tags: extractedTags,
          cases: caseCards,
        });
      }
      throw err;
    }
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
