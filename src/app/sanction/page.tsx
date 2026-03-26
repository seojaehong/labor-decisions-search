'use client';

import { useState, useRef, useEffect, type FormEvent } from 'react';
import { Send, Bot, User, Loader2, Scale, CheckCircle2, GitCompareArrows, ClipboardList } from 'lucide-react';
import { PromptSuggestion } from '@/components/ui/prompt-suggestion';

interface CaseCard {
  id: string;
  title: string;
  decision_result: string;
  holding_summary?: string;
  holding_points: string;
  url: string;
  summary_short?: string;
  key_issue?: string;
  bucket?: 'worker_win' | 'employer_win' | 'other';
}

interface ComparisonMeta {
  issueSummary: string[];
  workerWinCases: CaseCard[];
  employerWinCases: CaseCard[];
  coreDifferences: string[];
  checklist: string[];
  decisionGuide: string[];
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tags?: string[];
  cases?: CaseCard[];
  comparison?: ComparisonMeta | null;
}

const RESULT_LABELS: Record<string, string> = {
  granted: '인용',
  dismissed: '기각',
  rejected: '각하',
  upheld: '초심유지',
  overturned: '초심취소',
  settled: '화해/취하',
  partial: '일부인정',
  other: '기타',
};

const RESULT_COLORS: Record<string, string> = {
  granted: 'bg-green-100 text-green-700',
  dismissed: 'bg-red-100 text-red-700',
  rejected: 'bg-gray-100 text-gray-600',
  upheld: 'bg-blue-100 text-blue-700',
  overturned: 'bg-purple-100 text-purple-700',
  settled: 'bg-orange-100 text-orange-700',
  partial: 'bg-yellow-100 text-yellow-700',
};

const QUICK_REPLIES = [
  '직원이 회사 물품을 횡령했습니다',
  '반복적으로 무단결근하는 직원',
  '직장 내 폭언/폭행 사건',
  '업무 성과가 현저히 부족한 직원',
  '직장 내 성희롱이 발생했습니다',
  '사내 기밀정보를 외부에 유출한 경우',
];

export default function SanctionPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastError, setLastError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  async function requestAnalysis(updatedMessages: Message[]) {
    setLoading(true);
    setLastError(null);

    try {
      const res = await fetch('/api/sanction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages }),
      });

      const raw = await res.text();
      let data: { content?: string; tags?: string[]; cases?: CaseCard[]; comparison?: ComparisonMeta | null } | null = null;

      try {
        data = raw ? JSON.parse(raw) : {};
      } catch {
        throw new Error(raw || '응답 형식을 해석할 수 없습니다.');
      }

      if (!res.ok) {
        throw new Error(data?.content || `요청 처리에 실패했습니다. (${res.status})`);
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.content || '분석 결과를 생성할 수 없습니다.',
          tags: data.tags,
          cases: data.cases,
          comparison: data.comparison,
        },
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : '오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
      setLastError(message);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: text.trim() };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');

    await requestAnalysis(updatedMessages);
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    sendMessage(input);
  }

  const isEmpty = messages.length === 0;

  const displayMessages = messages;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      {/* Header */}
      <div className="mb-6 text-center">
        <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-blue-50 px-4 py-1.5">
          <Scale size={14} className="text-blue-600" />
          <span className="text-xs font-medium text-blue-700">42,000건 노동위 판정례 기반</span>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">AI 판정례 비교분석</h1>
        <p className="mt-1 text-sm text-gray-500">
          상황을 설명하시면 유사 판정례를 비교해 승패를 가른 요소와 실무 체크리스트를 안내합니다
        </p>
      </div>

      {/* Chat Area */}
      <div className="flex flex-col rounded-2xl border border-gray-200 bg-white shadow-sm" style={{ height: 'calc(100vh - 240px)', minHeight: '500px' }}>
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-5">
          {/* Empty State */}
          {isEmpty && !loading && (
            <div className="flex h-full flex-col items-center justify-center">
              <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50">
                <Scale size={28} className="text-blue-600" />
              </div>
              <p className="mb-1 text-lg font-semibold text-gray-800">어떤 상황이신가요?</p>
              <p className="mb-8 text-sm text-gray-400">징계 사유를 설명해 주시면 유사 판정례를 분석해 드립니다</p>
              <div className="flex max-w-lg flex-wrap justify-center gap-2">
                {QUICK_REPLIES.map((text) => (
                  <PromptSuggestion key={text} onClick={() => sendMessage(text)}>
                    {text}
                  </PromptSuggestion>
                ))}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="space-y-5">
            {displayMessages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                    msg.role === 'user' ? 'bg-blue-100' : 'bg-gray-100'
                  }`}
                >
                  {msg.role === 'user' ? (
                    <User size={14} className="text-blue-600" />
                  ) : (
                    <Bot size={14} className="text-gray-600" />
                  )}
                </div>
                <div className={`max-w-[85%] space-y-3 ${msg.role === 'user' ? 'text-right' : ''}`}>
                  {/* User message */}
                  {msg.role === 'user' && (
                    <div className="inline-block rounded-2xl bg-blue-600 px-4 py-3 text-sm text-white">
                      {msg.content}
                    </div>
                  )}

                  {msg.role === 'assistant' && msg.content && !msg.comparison && (
                    <div className="rounded-2xl bg-gray-50 px-4 py-3 text-sm leading-relaxed text-gray-800 whitespace-pre-wrap">
                      {msg.content}
                    </div>
                  )}

                  {msg.comparison && (
                    <div className="space-y-4">
                      {msg.comparison.issueSummary.length > 0 && (
                        <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4">
                          <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-blue-900">
                            <Scale size={15} />
                            쟁점 요약
                          </div>
                          <div className="space-y-1 text-sm text-blue-900">
                            {msg.comparison.issueSummary.map((item, idx) => (
                              <p key={`issue-${idx}`}>{item}</p>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="grid gap-4 md:grid-cols-2">
                        <div className="rounded-2xl border border-green-200 bg-green-50 p-4">
                          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-green-900">
                            <GitCompareArrows size={15} />
                            근로자가 이긴 사건
                          </div>
                          <div className="space-y-3">
                            {msg.comparison.workerWinCases.length > 0 ? msg.comparison.workerWinCases.map((c) => (
                              <a
                                key={c.id}
                                href={c.url || `/decisions/${c.id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block rounded-xl border border-green-200 bg-white p-3 hover:bg-green-100/40"
                              >
                                <div className="mb-1 text-xs font-semibold text-green-700">{c.title}</div>
                                <p className="text-xs leading-relaxed text-gray-700">{c.holding_points || c.summary_short || c.key_issue}</p>
                              </a>
                            )) : <p className="text-xs text-gray-500">직접 비교 가능한 인용 사건이 아직 충분하지 않습니다.</p>}
                          </div>
                        </div>

                        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4">
                          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-rose-900">
                            <GitCompareArrows size={15} />
                            사용자가 이긴 사건
                          </div>
                          <div className="space-y-3">
                            {msg.comparison.employerWinCases.length > 0 ? msg.comparison.employerWinCases.map((c) => (
                              <a
                                key={c.id}
                                href={c.url || `/decisions/${c.id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block rounded-xl border border-rose-200 bg-white p-3 hover:bg-rose-100/40"
                              >
                                <div className="mb-1 text-xs font-semibold text-rose-700">{c.title}</div>
                                <p className="text-xs leading-relaxed text-gray-700">{c.holding_points || c.summary_short || c.key_issue}</p>
                              </a>
                            )) : <p className="text-xs text-gray-500">직접 비교 가능한 기각 사건이 아직 충분하지 않습니다.</p>}
                          </div>
                        </div>
                      </div>

                      {msg.comparison.coreDifferences.length > 0 && (
                        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-amber-900">
                            <CheckCircle2 size={15} />
                            승패를 가른 핵심 차이
                          </div>
                          <ul className="space-y-2 text-sm text-amber-950">
                            {msg.comparison.coreDifferences.map((item, idx) => (
                              <li key={`diff-${idx}`}>- {item}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {msg.comparison.checklist.length > 0 && (
                        <div className="rounded-2xl border border-gray-200 bg-white p-4">
                          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-gray-900">
                            <ClipboardList size={15} />
                            실무 체크리스트
                          </div>
                          <div className="grid gap-2 md:grid-cols-2">
                            {msg.comparison.checklist.map((item, idx) => (
                              <div key={`check-${idx}`} className="rounded-xl bg-gray-50 px-3 py-2 text-sm text-gray-700">
                                {item}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {msg.comparison.decisionGuide.length > 0 && (
                        <div className="rounded-2xl border border-purple-200 bg-purple-50 p-4">
                          <div className="mb-3 text-sm font-semibold text-purple-900">문안/의사결정 보조</div>
                          <div className="space-y-2 text-sm text-purple-950">
                            {msg.comparison.decisionGuide.map((item, idx) => (
                              <p key={`guide-${idx}`}>{item}</p>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Assistant: Case Cards */}
                  {msg.cases && msg.cases.length > 0 && (() => {
                    const comparisonIds = new Set([
                      ...(msg.comparison?.workerWinCases.map((c) => c.id) || []),
                      ...(msg.comparison?.employerWinCases.map((c) => c.id) || []),
                    ]);
                    const extraCases = msg.cases.filter((c) => !comparisonIds.has(c.id));

                    if (extraCases.length === 0) return null;

                    return (
                    <div className="space-y-2">
                      <span className="text-xs font-medium text-gray-500">추가 참고 판정례</span>
                      {extraCases.map((c) => (
                        <a
                          key={c.id}
                          href={c.url || `/decisions/${c.id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block rounded-xl border border-gray-200 p-3 transition-colors hover:border-blue-300 hover:bg-blue-50/30"
                        >
                          <div className="mb-2 flex items-center justify-between gap-2">
                              <div className="text-xs font-medium text-gray-800 line-clamp-1">{c.title}</div>
                              <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${RESULT_COLORS[c.decision_result] || 'bg-gray-100 text-gray-600'}`}>
                                {RESULT_LABELS[c.decision_result] || c.decision_result}
                              </span>
                          </div>
                          <p className="text-xs text-gray-600 line-clamp-2">
                            {c.holding_points || c.summary_short || c.holding_summary || c.title}
                          </p>
                        </a>
                      ))}
                    </div>
                    );
                  })()}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100">
                  <Loader2 size={14} className="animate-spin text-gray-500" />
                </div>
                <div className="rounded-2xl bg-gray-50 px-4 py-3 text-sm text-gray-400">
                  판정례 비교분석 중...
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="border-t border-gray-100 px-4 py-1.5">
          <p className="text-center text-[10px] text-gray-400">
            본 결과는 유사 판정례 비교에 기반한 참고용입니다. 최종 결정 전 반드시 노무사와 상담하세요.
          </p>
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="flex gap-2 border-t border-gray-200 p-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="징계 상황을 설명해 주세요..."
            className="flex-1 rounded-xl border border-gray-200 px-4 py-2.5 text-sm outline-none transition-colors focus:border-blue-400"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex items-center justify-center rounded-xl bg-blue-600 px-4 text-white transition-colors hover:bg-blue-700 disabled:bg-gray-300"
          >
            <Send size={16} />
          </button>
        </form>
        {lastError && (
          <div className="border-t border-gray-100 px-4 pb-4">
            <p className="mb-2 text-xs text-red-500">{lastError}</p>
            <button
              type="button"
              onClick={() => {
                const lastAssistantIndex = [...messages].reverse().findIndex((message) => message.role === 'assistant');
                if (lastAssistantIndex === -1) return;

                const assistantIndex = messages.length - 1 - lastAssistantIndex;
                const retryMessages = messages.slice(0, assistantIndex);
                if (retryMessages.some((message) => message.role === 'user')) {
                  void requestAnalysis(retryMessages);
                }
              }}
              className="rounded-lg border border-gray-200 px-3 py-2 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50"
            >
              다시 시도
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
