export type HoldingBlockKind =
  | "level1"
  | "level2"
  | "level3"
  | "numbered"
  | "bullet"
  | "paragraph";

export interface HoldingBlock {
  kind: HoldingBlockKind;
  text: string;
  indent: 0 | 1 | 2;
}

// 가나다 순번만 매칭 (가~하). "습니다." 같은 문장 끝이 줄바꿈 후 "다."로 잘려 매칭되는 것을 방지
const LEVEL1_PATTERN = /^[가나다라마바사아자차카타파하]\.\s+/;
const LEVEL2_PATTERN = /^\(\d+\)\s+/;
const LEVEL3_PATTERN = /^[①-⑳]\s*/;
const NUMBERED_PATTERN = /^\d+\.\s+/;
const BULLET_PATTERN = /^[-·]\s+/;

export function stripMarkdownFormatting(input: string): string {
  return input
    // Strip markdown headers → plain text
    .replace(/^#{1,4}\s+(.+)$/gm, '$1')
    // Strip bold markers ** **
    .replace(/\*\*(.+?)\*\*/g, '$1')
    // Strip italic markers * *
    .replace(/\*(.+?)\*/g, '$1')
    // Strip □ prefix used in some decisions
    .replace(/^□\s*/gm, '');
}

// 가나다 순번 문자 목록
const GANADA = '가나다라마바사아자차카타파하';

// 가나다 마커 앞 글자가 한글이면 분리하지 않음 (문장 끝 "~다.", "~나." 등 오탐 방지)
// 한글이 아닌 경우(마침표, 공백, 숫자 등)만 구조적 줄바꿈 삽입
function injectStructuralBreaks(input: string): string {
  return input
    .replace(
      new RegExp(`([^\\n])(?=[${GANADA}]\\.\\s)`, 'g'),
      (match, prev) => /[가-힣]/.test(prev) ? match : prev + '\n'
    )
    .replace(/\s*(?=(\(\d+\)\s+\S{2,}))/g, (match, _marker, offset) => (offset === 0 ? "" : "\n"))
    .replace(/\s*(?=([①-⑳]\s*\S{2,}))/g, (match, _marker, offset) => (offset === 0 ? "" : "\n"));
}

function clampIndent(value: number): 0 | 1 | 2 {
  if (value <= 0) return 0;
  if (value === 1) return 1;
  return 2;
}

export function parseHoldingText(input: string | null | undefined): HoldingBlock[] {
  if (!input) return [];

  const normalizedInput = injectStructuralBreaks(stripMarkdownFormatting(input));

  const lines = normalizedInput
    .split(/\r?\n/)
    .map((line) => line.trimEnd())
    .filter((line) => line.trim().length > 0);

  const blocks: HoldingBlock[] = [];
  let lastStructuralIndent: 0 | 1 | 2 = 0;

  for (const rawLine of lines) {
    const line = rawLine.trimStart();

    if (LEVEL1_PATTERN.test(line)) {
      blocks.push({ kind: "level1", text: line, indent: 0 });
      lastStructuralIndent = 0;
      continue;
    }

    if (LEVEL2_PATTERN.test(line)) {
      blocks.push({ kind: "level2", text: line, indent: 1 });
      lastStructuralIndent = 1;
      continue;
    }

    if (LEVEL3_PATTERN.test(line)) {
      blocks.push({ kind: "level3", text: line, indent: 2 });
      lastStructuralIndent = 2;
      continue;
    }

    if (NUMBERED_PATTERN.test(line)) {
      const indent = blocks.length > 0 && blocks[blocks.length - 1]?.kind === "level1" ? 1 : 0;
      blocks.push({ kind: "numbered", text: line, indent });
      lastStructuralIndent = indent;
      continue;
    }

    if (BULLET_PATTERN.test(line)) {
      const indent = clampIndent(lastStructuralIndent + 1);
      blocks.push({ kind: "bullet", text: line, indent });
      lastStructuralIndent = indent;
      continue;
    }

    const previous = blocks[blocks.length - 1];
    const indent = previous?.kind === "paragraph"
      ? previous.indent
      : clampIndent(lastStructuralIndent + 1);

    blocks.push({ kind: "paragraph", text: line, indent });
  }

  return blocks;
}
