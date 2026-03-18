'use client';

import { useState, useRef, useEffect, type FormEvent } from 'react';
import { Send, Bot, User, Loader2, Scale, ExternalLink } from 'lucide-react';
import { PromptSuggestion } from '@/components/ui/prompt-suggestion';
import { Badge } from '@/components/ui/badge';

interface CaseCard {
  id: string;
  title: string;
  decision_result: string;
  holding_points: string;
  url: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tags?: string[];
  cases?: CaseCard[];
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
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: text.trim() };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/sanction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages }),
      });

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.content,
          tags: data.tags,
          cases: data.cases,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '오류가 발생했습니다. 잠시 후 다시 시도해 주세요.' },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    sendMessage(input);
  }

  const isEmpty = messages.length === 0;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      {/* Header */}
      <div className="mb-6 text-center">
        <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-blue-50 px-4 py-1.5">
          <Scale size={14} className="text-blue-600" />
          <span className="text-xs font-medium text-blue-700">42,000건 노동위 판정례 기반</span>
        </div>
        <h1 className="text-2xl font-bold text-gray-900">AI 징계양정 추천</h1>
        <p className="mt-1 text-sm text-gray-500">
          상황을 설명하시면 유사 판정례를 분석하여 예상 징계수위와 절차를 안내합니다
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
            {messages.map((msg, i) => (
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

                  {/* Assistant: Tags - hidden */}

                  {/* Assistant: Content */}
                  {msg.role === 'assistant' && (
                    <div className="rounded-2xl bg-gray-50 px-4 py-3 text-sm leading-relaxed text-gray-800 whitespace-pre-wrap">
                      {msg.content}
                    </div>
                  )}

                  {/* Assistant: Case Cards */}
                  {msg.cases && msg.cases.length > 0 && (
                    <div className="space-y-2">
                      <span className="text-xs font-medium text-gray-500">근거 판정례</span>
                      {msg.cases.map((c) => (
                        <a
                          key={c.id}
                          href={c.url || `/decisions/${c.id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block rounded-xl border border-gray-200 p-3 transition-colors hover:border-blue-300 hover:bg-blue-50/30"
                        >
                          <div className="mb-1 flex items-center justify-end">
                              <span className={`rounded-full px-2 py-0.5 text-[10px] font-medium ${RESULT_COLORS[c.decision_result] || 'bg-gray-100 text-gray-600'}`}>
                                {RESULT_LABELS[c.decision_result] || c.decision_result}
                              </span>
                          </div>
                          <p className="text-xs text-gray-600 line-clamp-2">{c.holding_points || c.title}</p>
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100">
                  <Loader2 size={14} className="animate-spin text-gray-500" />
                </div>
                <div className="rounded-2xl bg-gray-50 px-4 py-3 text-sm text-gray-400">
                  42,000건 판정례 분석 중...
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="border-t border-gray-100 px-4 py-1.5">
          <p className="text-center text-[10px] text-gray-400">
            본 결과는 노동위 판정례 통계에 기반한 참고용이며, 최종 결정 전 반드시 노무사와 상담하세요.
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
      </div>
    </div>
  );
}
