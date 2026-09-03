#!/usr/bin/env python3
# ===============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# Truth. Dignity. Protection. Transparency. No Erasure.
# ===============================================================================
"""
porch_ear.py — Porch
Turns one WAV catch into words on this machine.

Author: Everett Christman / The Christman AI Project
Cardinal Rules: All 15 apply. Rule 13 is gospel.

The model path comes from VOSK_MODEL_PATH.
That folder is on this machine. Nothing is fetched.
Nothing is borrowed from another being.
Text is empty unless the recognizer produced words.
"""

from __future__ import annotations

import io
import json
import os
import sys
import wave
from typing import Any, Dict, Optional


class EarUnavailable(RuntimeError):
    """The ear cannot sit. Say so. Do not invent speech."""


def model_path() -> str:
    path = (os.environ.get("VOSK_MODEL_PATH") or "").strip()
    if not path:
        raise EarUnavailable(
            "VOSK_MODEL_PATH is not set. The model stays on this machine."
        )
    if not os.path.isdir(path):
        raise EarUnavailable(f"VOSK_MODEL_PATH is not a folder: {path}")
    return path


def pcm_from_wav(blob: bytes) -> tuple[bytes, int, int]:
    try:
        with wave.open(io.BytesIO(blob), "rb") as wf:
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
    except wave.Error as exc:
        raise ValueError(f"not a WAV: {exc}") from exc
    if channels != 1:
        raise ValueError(f"Porch wants mono WAV, got {channels} channels")
    if width != 2:
        raise ValueError(f"Porch wants 16-bit PCM, got {width * 8}-bit")
    if not frames:
        raise ValueError("WAV contained no frames")
    return frames, rate, width


def hear_wav(blob: bytes) -> Dict[str, Any]:
    """
    Recognize one WAV. Returns a dict.
    text is empty on every failure. Diagnostics live in error.
    """
    try:
        pcm, rate, _width = pcm_from_wav(blob)
    except ValueError as exc:
        return {"ok": False, "text": "", "error": str(exc)}

    try:
        path = model_path()
    except EarUnavailable as exc:
        return {"ok": False, "text": "", "error": str(exc)}

    try:
        import vosk
    except ImportError:
        return {
            "ok": False,
            "text": "",
            "error": "vosk is not installed on this machine",
        }

    try:
        vosk.SetLogLevel(-1)
        rec = vosk.KaldiRecognizer(vosk.Model(path), float(rate))
        rec.SetWords(True)
        rec.AcceptWaveform(pcm)
        payload = json.loads(rec.FinalResult())
    except Exception as exc:
        return {"ok": False, "text": "", "error": str(exc)}

    text = (payload.get("text") or "").strip()
    if not text:
        return {"ok": False, "text": "", "error": "no words"}
    return {"ok": True, "text": text, "error": None}


def hear_file(path: str) -> Dict[str, Any]:
    try:
        with open(path, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        return {"ok": False, "text": "", "error": str(exc)}
    return hear_wav(blob)


def main(argv: Optional[list[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(
            json.dumps(
                {
                    "ok": False,
                    "text": "",
                    "error": "pass a WAV path",
                }
            )
        )
        return 2
    result = hear_file(args[0])
    print(json.dumps(result))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
