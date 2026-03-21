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

const LEVEL1_PATTERN = /^[가-힣]\.\s+/;
const LEVEL2_PATTERN = /^\(\d+\)\s+/;
const LEVEL3_PATTERN = /^[①-⑳]\s*/;
const NUMBERED_PATTERN = /^\d+\.\s+/;
const BULLET_PATTERN = /^[-·]\s+/;

function injectStructuralBreaks(input: string): string {
  return input
    .replace(/\s*(?=([가-힣]\.\s+\S{2,}))/g, (match, marker, offset) => (offset === 0 ? "" : "\n"))
    .replace(/\s*(?=(\(\d+\)\s+\S{2,}))/g, (match, marker, offset) => (offset === 0 ? "" : "\n"))
    .replace(/\s*(?=([①-⑳]\s*\S{2,}))/g, (match, marker, offset) => (offset === 0 ? "" : "\n"));
}

function clampIndent(value: number): 0 | 1 | 2 {
  if (value <= 0) return 0;
  if (value === 1) return 1;
  return 2;
}

export function parseHoldingText(input: string | null | undefined): HoldingBlock[] {
  if (!input) return [];

  const normalizedInput = injectStructuralBreaks(input);

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
