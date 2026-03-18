import Link from "next/link";
import { Card } from "@/components/ui/card";
import { REASON_LABELS, type ReasonCategory } from "@/lib/types";

const REASON_ICONS: Record<ReasonCategory, string> = {
  sexual_harassment: "🚫",
  workplace_bullying: "😤",
  violence: "👊",
  absence: "🚪",
  embezzlement: "💰",
  incompetence: "📉",
  misconduct: "⚠️",
  redundancy: "🏢",
  probation: "📋",
  other: "📌",
};

export default function Home() {
  const categories = Object.entries(REASON_LABELS) as [ReasonCategory, string][];

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight mb-4">
            노동위원회 판정례 검색
          </h1>
          <p className="text-lg text-muted-foreground">
            부당해고 판정례 37,000건+ 사유/절차/양정 기준 구조화 DB
          </p>
        </div>

        <div className="mb-8">
          <Link href="/search">
            <div className="flex items-center border rounded-lg px-4 py-3 text-muted-foreground hover:border-primary transition-colors cursor-pointer">
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              판정례 검색...
            </div>
          </Link>
        </div>

        <h2 className="text-xl font-semibold mb-4">사유별 검색</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {categories.map(([key, label]) => (
            <Link key={key} href={`/search?reason=${key}`}>
              <Card className="p-4 text-center hover:border-primary transition-colors cursor-pointer">
                <div className="text-2xl mb-1">{REASON_ICONS[key]}</div>
                <div className="font-medium text-sm">{label}</div>
              </Card>
            </Link>
          ))}
        </div>

        <div className="mt-12 text-center text-sm text-muted-foreground">
          <p>데이터 출처: 법제처 국가법령정보센터 노동위원회 결정문</p>
          <p className="mt-1">
            <Link href="/stats" className="underline hover:text-primary">통계 보기</Link>
          </p>
        </div>
      </div>
    </main>
  );
}
