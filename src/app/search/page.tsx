"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useState, useEffect, Suspense } from "react";
import { supabase } from "@/lib/supabase";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  REASON_LABELS,
  RESULT_LABELS,
  type NlrcDecision,
  type ReasonCategory,
  type DecisionResult,
} from "@/lib/types";
import Link from "next/link";

const RESULT_COLORS: Record<DecisionResult, string> = {
  granted: "bg-green-100 text-green-800",
  partial: "bg-yellow-100 text-yellow-800",
  dismissed: "bg-red-100 text-red-800",
  rejected: "bg-gray-100 text-gray-800",
  upheld: "bg-blue-100 text-blue-800",
  overturned: "bg-purple-100 text-purple-800",
  settled: "bg-orange-100 text-orange-800",
};

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [reason, setReason] = useState<ReasonCategory | "">(
    (searchParams.get("reason") as ReasonCategory) || ""
  );
  const [result, setResult] = useState<DecisionResult | "">(
    (searchParams.get("result") as DecisionResult) || ""
  );
  const [decisions, setDecisions] = useState<NlrcDecision[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const PAGE_SIZE = 20;

  useEffect(() => {
    search();
  }, [reason, result, page]);

  async function search() {
    setLoading(true);
    let q = supabase
      .from("nlrc_decisions")
      .select("*", { count: "exact" })
      .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1)
      .order("decision_date", { ascending: false });

    if (reason) q = q.contains("reason_category", [reason]);
    if (result) q = q.eq("decision_result", result);
    if (query) q = q.textSearch("search_vector", query.split(" ").join(" & "));

    const { data, count, error } = await q;
    if (!error) {
      setDecisions(data || []);
      setTotal(count || 0);
    }
    setLoading(false);
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setPage(0);
    search();
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <Link href="/" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">
          &larr; 홈으로
        </Link>

        <h1 className="text-2xl font-bold mb-6">판정례 검색</h1>

        <form onSubmit={handleSearch} className="flex gap-2 mb-6">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="키워드 검색 (예: 성희롱, 수습해고, 서면통지)"
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
              onChange={(e) => { setReason(e.target.value as ReasonCategory); setPage(0); }}
            >
              <option value="">전체</option>
              {Object.entries(REASON_LABELS).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">판정결과</label>
            <select
              className="border rounded px-3 py-2 text-sm"
              value={result}
              onChange={(e) => { setResult(e.target.value as DecisionResult); setPage(0); }}
            >
              <option value="">전체</option>
              {Object.entries(RESULT_LABELS).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </select>
          </div>
        </div>

        <p className="text-sm text-muted-foreground mb-4">
          {loading ? "검색 중..." : `${total.toLocaleString()}건`}
        </p>

        <div className="space-y-3">
          {decisions.map((d) => (
            <Link key={d.id} href={`/decisions/${d.id}`}>
              <Card className="p-4 hover:border-primary transition-colors cursor-pointer mb-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-sm line-clamp-2">{d.title}</h3>
                    <p className="text-xs text-muted-foreground mt-1">
                      {d.department} | {d.decision_date}
                    </p>
                    {d.key_issue && (
                      <p className="text-xs mt-2 text-muted-foreground line-clamp-2">
                        {d.key_issue}
                      </p>
                    )}
                  </div>
                  <div className="flex flex-col gap-1 items-end shrink-0">
                    <Badge className={RESULT_COLORS[d.decision_result as DecisionResult] || ""}>
                      {RESULT_LABELS[d.decision_result as DecisionResult] || d.decision_result}
                    </Badge>
                    {d.reason_category?.map((r: string) => (
                      <Badge key={r} variant="outline" className="text-xs">
                        {REASON_LABELS[r as ReasonCategory] || r}
                      </Badge>
                    ))}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>

        {total > PAGE_SIZE && (
          <div className="flex justify-center gap-2 mt-8">
            <Button
              variant="outline"
              disabled={page === 0}
              onClick={() => setPage(p => p - 1)}
            >
              이전
            </Button>
            <span className="flex items-center text-sm text-muted-foreground">
              {page + 1} / {Math.ceil(total / PAGE_SIZE)}
            </span>
            <Button
              variant="outline"
              disabled={(page + 1) * PAGE_SIZE >= total}
              onClick={() => setPage(p => p + 1)}
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
