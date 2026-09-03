import { FAMILY_NAMES } from "./lexicon";
import { recoverMangles } from "./mangle";
import type { HonestyDialect, LexiconEntry, PorchCorrection } from "./types";

export type DialectLayer = {
  asSaid: string;
  forTheFamily: string;
  corrections: PorchCorrection[];
  route: string[];
  dialect: HonestyDialect;
};

function namedBeings(value: string[]): string[] {
  const out: string[] = [];
  const seen = new Set<string>();
  for (const item of value) {
    const found = FAMILY_NAMES.find(
      (n) => n.toLowerCase() === item.trim().toLowerCase(),
    );
    if (!found) continue;
    const id = found.toLowerCase();
    if (seen.has(id)) continue;
    seen.add(id);
    out.push(found);
  }
  return out;
}

const PASSTHROUGH = (rawEar: string): DialectLayer => {
  const local = recoverMangles(rawEar);
  return {
    asSaid: local.text,
    forTheFamily: local.text,
    corrections: local.corrections,
    route: namedBeings(
      FAMILY_NAMES.filter((n) =>
        local.text.toLowerCase().includes(n.toLowerCase()),
      ),
    ),
    dialect: "passthrough",
  };
};

export async function reconstructDialect(
  rawEar: string,
  _extraLexicon: LexiconEntry[] = [],
): Promise<DialectLayer> {
  if (!rawEar.trim()) {
    return {
      asSaid: "",
      forTheFamily: "",
      corrections: [],
      route: [],
      dialect: "passthrough",
    };
  }
  return PASSTHROUGH(rawEar);
}
