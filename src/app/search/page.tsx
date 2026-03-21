"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useState, useEffect, Suspense } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  REASON_LABELS,
  RESULT_LABELS,
  type ReasonCategory,
  type DecisionResult,
} from "@/lib/types";
import Link from "next/link";

type SearchMode = "baseline" | "candidate" | "compare";

interface SearchCard {
  id: string;
  title: string;
  department: string | null;
  decision_date: string | null;
  decision_result: string;
  key_issue: string | null;
  url: string | null;
  reason_category: string[];
  case_id?: string;
  employment_stage?: string | null;
  issue_type_primary?: string | null;
  issue_type_secondary?: string[];
  disposition_type?: string[];
  fact_markers?: string[];
  legal_focus?: string[];
  exclusion_flags?: string[];
  why_surfaced?: string[];
  score?: number | null;
}

interface SearchBucket {
  items: SearchCard[];
  total: number;
  page: number;
  pageSize: number;
}

interface SearchResponsePayload {
  mode: SearchMode;
  query: string;
  reason: ReasonCategory | "";
  result: DecisionResult | "";
  baseline?: SearchBucket;
  candidate?: SearchBucket;
}

const RESULT_COLORS: Record<string, string> = {
  granted: "bg-green-100 text-green-800",
  partial: "bg-yellow-100 text-yellow-800",
  dismissed: "bg-red-100 text-red-800",
  rejected: "bg-gray-100 text-gray-800",
  upheld: "bg-blue-100 text-blue-800",
  overturned: "bg-purple-100 text-purple-800",
  settled: "bg-orange-100 text-orange-800",
};

function SearchModeButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <Button variant={active ? "default" : "outline"} onClick={onClick} type="button">
      {children}
    </Button>
  );
}

function DebugBadge({ label }: { label: string }) {
  return (
    <Badge variant="outline" className="text-[11px]">
      {label}
    </Badge>
  );
}

function SearchResultCard({ item, source }: { item: SearchCard; source: "baseline" | "candidate" }) {
  return (
    <Link key={`${source}-${item.id}`} href={`/decisions/${item.id}`}>
      <Card className="p-4 hover:border-primary transition-colors cursor-pointer mb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-sm line-clamp-2">{item.title}</h3>
            <p className="text-xs text-muted-foreground mt-1">
              {item.department || "-"} | {item.decision_date || "-"} | {item.case_id || item.id}
            </p>
            {item.key_issue && (
              <p className="text-xs mt-2 text-muted-foreground line-clamp-2">{item.key_issue}</p>
            )}
            {source === "candidate" && (
              <div className="flex flex-wrap gap-1 mt-3">
                {item.issue_type_primary && <DebugBadge label={`primary:${item.issue_type_primary}`} />}
                {item.employment_stage && <DebugBadge label={`stage:${item.employment_stage}`} />}
                {(item.disposition_type || []).slice(0, 2).map((value) => (
                  <DebugBadge key={value} label={`disp:${value}`} />
                ))}
                {typeof item.score === "number" && <DebugBadge label={`score:${item.score}`} />}
              </div>
            )}
            {item.why_surfaced && item.why_surfaced.length > 0 && (
              <p className="text-[11px] mt-2 text-muted-foreground line-clamp-2">
                why: {item.why_surfaced.slice(0, 4).join(", ")}
              </p>
            )}
          </div>
          <div className="flex flex-col gap-1 items-end shrink-0">
            <Badge className={RESULT_COLORS[item.decision_result] || ""}>
              {RESULT_LABELS[item.decision_result as DecisionResult] || item.decision_result}
            </Badge>
            {(item.reason_category || []).slice(0, 2).map((reason) => (
              <Badge key={reason} variant="outline" className="text-xs">
                {REASON_LABELS[reason as ReasonCategory] || reason}
              </Badge>
            ))}
          </div>
        </div>
      </Card>
    </Link>
  );
}

function SearchBucketSection({
  title,
  bucket,
  source,
}: {
  title: string;
  bucket?: SearchBucket;
  source: "baseline" | "candidate";
}) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold">{title}</h2>
        <span className="text-sm text-muted-foreground">{bucket?.total?.toLocaleString() || 0}건</span>
      </div>
      <div className="space-y-3">
        {(bucket?.items || []).map((item) => (
          <SearchResultCard key={`${source}-${item.id}`} item={item} source={source} />
        ))}
        {(!bucket || bucket.items.length === 0) && (
          <Card className="p-4 text-sm text-muted-foreground">결과가 없습니다.</Card>
        )}
      </div>
    </div>
  );
}

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [queryInput, setQueryInput] = useState(searchParams.get("q") || "");
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [reason, setReason] = useState<ReasonCategory | "">((searchParams.get("reason") as ReasonCategory) || "");
  const [result, setResult] = useState<DecisionResult | "">((searchParams.get("result") as DecisionResult) || "");
  const [mode, setMode] = useState<SearchMode>((searchParams.get("mode") as SearchMode) || "baseline");
  const [page, setPage] = useState(Number(searchParams.get("page") || "0"));
  const [loading, setLoading] = useState(true);
  const [payload, setPayload] = useState<SearchResponsePayload | null>(null);

  function syncUrl(next: {
    q?: string;
    reason?: ReasonCategory | "";
    result?: DecisionResult | "";
    mode?: SearchMode;
    page?: number;
  }) {
    const params = new URLSearchParams(searchParams.toString());
    const q = next.q ?? query;
    const nextReason = next.reason ?? reason;
    const nextResult = next.result ?? result;
    const nextMode = next.mode ?? mode;
    const nextPage = next.page ?? page;

    if (q) params.set("q", q);
    else params.delete("q");
    if (nextReason) params.set("reason", nextReason);
    else params.delete("reason");
    if (nextResult) params.set("result", nextResult);
    else params.delete("result");
    params.set("mode", nextMode);
    if (nextPage > 0) params.set("page", String(nextPage));
    else params.delete("page");

    router.replace(`/search?${params.toString()}`);
  }

  useEffect(() => {
    const urlQuery = searchParams.get("q") || "";
    const urlReason = (searchParams.get("reason") as ReasonCategory) || "";
    const urlResult = (searchParams.get("result") as DecisionResult) || "";
    const urlMode = (searchParams.get("mode") as SearchMode) || "baseline";
    const urlPage = Number(searchParams.get("page") || "0");

    setQueryInput(urlQuery);
    setQuery(urlQuery);
    setReason(urlReason);
    setResult(urlResult);
    setMode(urlMode);
    setPage(urlPage);
  }, [searchParams]);

  useEffect(() => {
    let aborted = false;

    async function fetchSearch() {
      setLoading(true);
      const params = new URLSearchParams({
        q: query,
        mode,
        page: String(page),
      });
      if (reason) params.set("reason", reason);
      if (result) params.set("result", result);

      const resp = await fetch(`/api/search?${params.toString()}`, { cache: "no-store" });
      const data = await resp.json();
      if (!aborted) {
        setPayload(data);
        setLoading(false);
      }
    }

    fetchSearch();
    return () => {
      aborted = true;
    };
  }, [query, reason, result, page, mode]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setPage(0);
    setQuery(queryInput);
    syncUrl({ q: queryInput, page: 0 });
  }

  function handleModeChange(nextMode: SearchMode) {
    setMode(nextMode);
    setPage(0);
    syncUrl({ mode: nextMode, page: 0 });
  }

  const baselineBucket = payload?.baseline;
  const candidateBucket = payload?.candidate;
  const total = mode === "candidate" ? candidateBucket?.total || 0 : baselineBucket?.total || 0;

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Link href="/" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">
          &larr; 홈으로
        </Link>

        <h1 className="text-2xl font-bold mb-3">판정례 검색</h1>
        <p className="text-sm text-muted-foreground mb-6">
          baseline은 기존 reason_category 검색, candidate는 8축 태그 retrieval, compare는 둘을 나란히 보여줍니다.
        </p>

        <div className="flex gap-2 mb-6">
          <SearchModeButton active={mode === "baseline"} onClick={() => handleModeChange("baseline")}>
            baseline
          </SearchModeButton>
          <SearchModeButton active={mode === "candidate"} onClick={() => handleModeChange("candidate")}>
            candidate
          </SearchModeButton>
          <SearchModeButton active={mode === "compare"} onClick={() => handleModeChange("compare")}>
            compare
          </SearchModeButton>
        </div>

        <form onSubmit={handleSearch} className="flex gap-2 mb-6">
          <Input
            value={queryInput}
            onChange={(e) => setQueryInput(e.target.value)}
            placeholder="키워드 검색 (예: 무단결근 절차위반, 괴롭힘 신고 보복, 정규직 저성과)"
            className="flex-1"
          />
          <Button type="submit">검색</Button>
        </form>

        <div className="flex flex-wrap gap-4 mb-6">
          <div>
            <label className="text-sm font-medium mb-1 block">사유</label>
            <select
              className="border rounded px-3 py-2 text-sm"
              value={reason}
              onChange={(e) => {
                const next = e.target.value as ReasonCategory | "";
                setReason(next);
                setPage(0);
                syncUrl({ reason: next, page: 0 });
              }}
            >
              <option value="">전체</option>
              {Object.entries(REASON_LABELS).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">판정결과</label>
            <select
              className="border rounded px-3 py-2 text-sm"
              value={result}
              onChange={(e) => {
                const next = e.target.value as DecisionResult | "";
                setResult(next);
                setPage(0);
                syncUrl({ result: next, page: 0 });
              }}
            >
              <option value="">전체</option>
              {Object.entries(RESULT_LABELS).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </div>
        </div>

        <p className="text-sm text-muted-foreground mb-4">
          {loading ? "검색 중..." : `${total.toLocaleString()}건`}
        </p>

        {mode === "compare" ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SearchBucketSection title="Baseline" bucket={baselineBucket} source="baseline" />
            <SearchBucketSection title="Candidate" bucket={candidateBucket} source="candidate" />
          </div>
        ) : mode === "candidate" ? (
          <SearchBucketSection title="Candidate" bucket={candidateBucket} source="candidate" />
        ) : (
          <SearchBucketSection title="Baseline" bucket={baselineBucket} source="baseline" />
        )}

        {mode === "baseline" && baselineBucket && baselineBucket.total > baselineBucket.pageSize && (
          <div className="flex justify-center gap-2 mt-8">
            <Button
              variant="outline"
              disabled={page === 0}
              onClick={() => {
                const next = page - 1;
                setPage(next);
                syncUrl({ page: next });
              }}
            >
              이전
            </Button>
            <span className="flex items-center text-sm text-muted-foreground">
              {page + 1} / {Math.ceil(baselineBucket.total / baselineBucket.pageSize)}
            </span>
            <Button
              variant="outline"
              disabled={(page + 1) * baselineBucket.pageSize >= baselineBucket.total}
              onClick={() => {
                const next = page + 1;
                setPage(next);
                syncUrl({ page: next });
              }}
            >
              다음
            </Button>
          </div>
        )}
      </div>
    </main>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="p-8">로딩 중...</div>}>
      <SearchContent />
    </Suspense>
  );
}
