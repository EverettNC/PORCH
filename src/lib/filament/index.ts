/**
 * Filament is its own house.
 * https://github.com/EverettNC/THEFILAMENT
 *
 * The cochlea, the fibers, the catch canvas — that is THEFILAMENT.
 * This folder does not copy that engine. Porch hears words.
 * Filament catches. Vosk sits in Filament's ear, offline.
 * Whisper is not in this body. Whole House :9785 is not this nerve.
 */
export const FILAMENT_GITHUB = "https://github.com/EverettNC/THEFILAMENT";
export const FILAMENT_ORGAN = "filament" as const;

export { createMic, MAX_SECONDS } from "./mic";
export type { MicHandle } from "./mic";
export { encodeWav, concatFloat32, blobToBase64 } from "./wav";
export type {
  AudioBus,
  CatchRecord,
  FieldSettings,
  FieldStatus,
  SttWord,
  TranscribeResult,
} from "./types";
