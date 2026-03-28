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

function getDisplayCaseNumber(caseNumber?: string | null) {
  if (!caseNumber) return "";
  return /^id_/i.test(caseNumber) ? "" : caseNumber;
}

function getSourceStatusLabel(hasDetailedHoldingPoints: boolean, hasHoldingPoints: boolean) {
  if (hasDetailedHoldingPoints) return "서비스 내 추출 원문 제공";
  if (hasHoldingPoints) return "추출 원문 일부 제공";
  return "서비스 내 정리본 제공";
}

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

  const displayCaseNumber = getDisplayCaseNumber(d.case_number);
  const holdingPointsText = typeof d.holding_points === "string" ? d.holding_points.trim() : "";
  const holdingSummaryText = typeof d.holding_summary === "string" ? d.holding_summary.trim() : "";
  const keyIssueText = typeof d.key_issue === "string" ? d.key_issue.trim() : "";
  const hasDetailedHoldingPoints = holdingPointsText.length >= 50;
  const hasHoldingPoints = holdingPointsText.length > 0;
  const hasSummary = holdingSummaryText.length > 0;
  const hasSourceSection = hasHoldingPoints || Boolean(d.url);

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-3xl mx-auto px-4 py-8">
        <Link href="/search" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">
          &larr; 검색으로
        </Link>

        <h1 className="text-xl font-bold mb-2">{d.title}</h1>
        <p className="text-sm text-muted-foreground mb-4">
          {d.department} | {d.decision_date}
          {displayCaseNumber ? ` | ${displayCaseNumber}` : ""}
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

        <Card className="p-4 mb-6 bg-muted/30">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="space-y-2">
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline">상세 페이지</Badge>
                <Badge variant="outline">{getSourceStatusLabel(hasDetailedHoldingPoints, hasHoldingPoints)}</Badge>
              </div>
              <p className="text-sm text-muted-foreground">
                이 페이지에서 판정요지와 절차 정보를 확인할 수 있습니다. 아래에서 추출 본문과 정리본을 검토하세요.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <a
                href="#decision-summary"
                className="inline-flex items-center rounded-md border px-3 py-2 text-sm font-medium hover:bg-muted"
              >
                요약 보기
              </a>
              {hasSourceSection ? (
                <a
                  href="#source-text"
                  className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground"
                >
                  원문·출처 보기
                </a>
              ) : null}
            </div>
          </div>
        </Card>

        {d.key_issue && (
          <Card id="decision-summary" className="p-4 mb-6 bg-muted/50 scroll-mt-24">
            <h3 className="font-semibold text-sm mb-1">핵심쟁점</h3>
            <p className="text-sm">{d.key_issue}</p>
          </Card>
        )}

        <section id={d.key_issue ? undefined : "decision-summary"} className="scroll-mt-24">
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

          {hasSummary && (
            <div className="mb-6">
              <h3 className="font-semibold mb-2">판정요지</h3>
              <div>{renderHoldingBlocks(holdingSummaryText)}</div>
            </div>
          )}
        </section>

        <Separator className="my-6" />

        <section id="source-text" className="scroll-mt-24">
          <div className="flex items-start justify-between gap-4 mb-3">
            <div>
              <h2 className="font-semibold">원문·출처</h2>
              <p className="text-sm text-muted-foreground mt-1">
                서비스 내 정리본과 추출된 본문 범위를 확인하세요.
              </p>
            </div>
            <Badge variant="outline">{getSourceStatusLabel(hasDetailedHoldingPoints, hasHoldingPoints)}</Badge>
          </div>

          {hasDetailedHoldingPoints ? (
            <Card className="p-4 mb-4">
              <h3 className="font-semibold text-sm mb-2">서비스 내 추출 원문</h3>
              <div>{renderHoldingBlocks(holdingPointsText)}</div>
            </Card>
          ) : (
            <Card className="p-4 mb-4 bg-muted/40">
              <h3 className="font-semibold text-sm mb-2">서비스 내 확인 가능한 내용</h3>
              <p className="text-sm text-muted-foreground mb-3">
                이 판정례는 상세한 추출 원문이 충분하지 않아, 아래 정리본을 제공합니다.
              </p>
              <div className="space-y-3">
                {hasHoldingPoints ? (
                  <div>
                    <p className="text-xs font-medium text-muted-foreground mb-1">추출된 원문 일부</p>
                    <div>{renderHoldingBlocks(holdingPointsText)}</div>
                  </div>
                ) : null}
                {hasSummary ? (
                  <div>
                    <p className="text-xs font-medium text-muted-foreground mb-1">판정요지 정리</p>
                    <div>{renderHoldingBlocks(holdingSummaryText)}</div>
                  </div>
                ) : null}
                {!hasHoldingPoints && !hasSummary && keyIssueText ? (
                  <div>
                    <p className="text-xs font-medium text-muted-foreground mb-1">핵심 쟁점 메모</p>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{keyIssueText}</p>
                  </div>
                ) : null}
              </div>
            </Card>
          )}

          <Card className="p-4 bg-muted/40">
            <p className="text-sm text-muted-foreground">
              위 판정요지와 정리본이 이 판정례의 핵심 내용입니다. 추가 검토가 필요하면 AI 비교분석을 활용하세요.
            </p>
          </Card>
        </section>
      </div>
    </main>
  );
}
