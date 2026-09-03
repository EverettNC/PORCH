/**
 * Porch — the word-ear.
 *
 * Corti measures pitch. Porch hears words.
 * The tape stays in this house unless Everett stands a local ear.
 * No rented cloud ear. No invented speech.
 *
 * Dialect is kept. SAE "correction" is a bug.
 */

export const PORCH_ORGAN = "porch" as const;
export const PORCH_FAMILY = "christman-sound" as const;

export type HonestyEar = "local" | "unavailable" | "sample" | "file";
export type HonestyDialect = "passthrough";

export type PorchCorrection = {
  from: string;
  to: string;
  why: string;
};

export type PorchTake = {
  id: string;
  at: number;
  durationMs: number;
  /** What was said. Dialect stays. */
  asSaid: string;
  /** Same meaning, family names recovered, still not SAE. */
  forTheFamily: string;
  /** Raw ear before the dialect layer. May be mangled. */
  rawEar: string;
  corrections: PorchCorrection[];
  route: string[];
  honesty: {
    ear: HonestyEar;
    dialect: HonestyDialect;
    corti: "not-this-nerve";
    cloud: boolean;
    rule: string;
  };
};

export type PorchPacket = {
  organ: typeof PORCH_ORGAN;
  family: typeof PORCH_FAMILY;
  kind: "utterance";
  take: PorchTake;
};

export type LexiconEntry = {
  said: string;
  keep: string;
  note: string;
};

export const PORCH_HONESTY_RULE =
  "Porch is the word-ear. The tape stays here. Dialect is kept. live is /laɪv/, not leave. Whisper is not in this body. A cloud ear is named if it is ever used. Empty ear stays empty.";
