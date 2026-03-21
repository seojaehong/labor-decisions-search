import { supabase } from "@/lib/supabase";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  REASON_LABELS,
  RESULT_LABELS,
  SANCTION_LABELS,
  type ReasonCategory,
  type DecisionResult,
  type SanctionType,
} from "@/lib/types";
import { parseHoldingText } from "@/lib/format-holding";
import { cn } from "@/lib/utils";
import Link from "next/link";

function renderHoldingBlocks(text: string) {
  return parseHoldingText(text).map((block, index) => (
    <p
      key={`${block.kind}-${index}`}
      className={cn(
        "text-sm leading-relaxed whitespace-pre-wrap",
        block.kind === "level1" && "font-semibold mt-4 first:mt-0",
        block.kind === "level2" && "pl-4 mt-2",
        block.kind === "level3" && "pl-8 mt-1.5",
        block.kind === "numbered" && (block.indent === 1 ? "pl-4 mt-2" : "font-semibold mt-4 first:mt-0"),
        block.kind === "bullet" && (block.indent === 2 ? "pl-8" : "pl-4"),
        block.kind === "paragraph" && (block.indent === 2 ? "pl-8" : block.indent === 1 ? "pl-4" : "")
      )}
    >
      {block.text}
    </p>
  ));
}

export default async function DecisionPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const { data: d } = await supabase
    .from("nlrc_decisions")
    .select("*")
    .eq("id", id)
    .single();

  if (!d) {
    return <div className="p-8">판정례를 찾을 수 없습니다.</div>;
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-3xl mx-auto px-4 py-8">
        <Link href="/search" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">
          &larr; 검색으로
        </Link>

        <h1 className="text-xl font-bold mb-2">{d.title}</h1>
        <p className="text-sm text-muted-foreground mb-4">
          {d.department} | {d.case_number} | {d.decision_date}
        </p>

        <div className="flex flex-wrap gap-2 mb-6">
          <Badge className="bg-blue-100 text-blue-800">
            {RESULT_LABELS[d.decision_result as DecisionResult] || d.decision_result}
          </Badge>
          {d.reason_category?.map((r: string) => (
            <Badge key={r} variant="outline">
              {REASON_LABELS[r as ReasonCategory] || r}
            </Badge>
          ))}
          <Badge variant="secondary">
            {SANCTION_LABELS[d.sanction_type as SanctionType] || d.sanction_type}
          </Badge>
        </div>

        {d.key_issue && (
          <Card className="p-4 mb-6 bg-muted/50">
            <h3 className="font-semibold text-sm mb-1">핵심쟁점</h3>
            <p className="text-sm">{d.key_issue}</p>
          </Card>
        )}

        {d.reason_detail && (
          <Card className="p-4 mb-4">
            <h3 className="font-semibold text-sm mb-1">해고 사유</h3>
            <p className="text-sm">{d.reason_detail}</p>
          </Card>
        )}

        <Card className="p-4 mb-4">
          <h3 className="font-semibold text-sm mb-2">절차 확인</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>{d.procedure_committee ? "✅" : "❌"} 징계위원회</div>
            <div>{d.procedure_defense ? "✅" : "❌"} 소명기회 부여</div>
            <div>{d.procedure_written_notice ? "✅" : "❌"} 서면통지</div>
            <div>{d.procedure_advance_notice ? "✅" : "❌"} 해고예고 30일</div>
          </div>
          {d.procedure_note && (
            <p className="text-xs text-muted-foreground mt-2">{d.procedure_note}</p>
          )}
        </Card>

        <Separator className="my-6" />

        {d.holding_points && (
          <div className="mb-6">
            <h3 className="font-semibold mb-2">판정사항</h3>
            <div>{renderHoldingBlocks(d.holding_points)}</div>
          </div>
        )}

        {d.holding_summary && (
          <div className="mb-6">
            <h3 className="font-semibold mb-2">판정요지</h3>
            <div>{renderHoldingBlocks(d.holding_summary)}</div>
          </div>
        )}

        {d.url && (
          <div className="mt-8 text-sm">
            <a
              href={d.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary underline"
            >
              원문 보기 (법제처)
            </a>
          </div>
        )}
      </div>
    </main>
  );
}
