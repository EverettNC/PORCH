/** Porch live take. The house rack may also hold this. */
import type { PorchTake } from "./types";

export type PorchLive = {
  organ: "porch";
  t: number;
  listening: boolean;
  take: PorchTake | null;
};

let porch: PorchLive | null = null;

export function setPorch(next: { listening?: boolean; take?: PorchTake | null }): PorchLive {
  const take = next.take && typeof next.take.id === "string" ? next.take : porch?.take ?? null;
  porch = {
    organ: "porch",
    t: Date.now(),
    listening: Boolean(next.listening),
    take,
  };
  return porch;
}

export function getPorch(): PorchLive | null {
  return porch;
}
