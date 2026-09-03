#!/usr/bin/env python3
# ===============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# Truth. Dignity. Protection. Transparency. No Erasure.
# ===============================================================================
"""
porch_ear.py — Porch
Hands one WAV to Christman-Sound SpeechRecognitionEngine.recognize_from_bytes.

Author: Everett Christman / The Christman AI Project
Cardinal Rules: All 15 apply. Rule 13 is gospel.

This file does not recognize. The package recognizes.
VOSK_MODEL_PATH is read by the package. This file does not invent a model path.
"""

from __future__ import annotations

import io
import json
import sys
import wave
from typing import Any, Dict, Optional


def pcm_from_wav(blob: bytes) -> tuple[bytes, int, int]:
    with wave.open(io.BytesIO(blob), "rb") as wf:
        channels = wf.getnchannels()
        width = wf.getsampwidth()
        rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
    if channels != 1:
        raise ValueError(f"Porch wants mono WAV, got {channels} channels")
    if width != 2:
        raise ValueError(f"Porch wants 16-bit PCM, got {width * 8}-bit")
    if not frames:
        raise ValueError("WAV contained no frames")
    return frames, rate, width


def hear_wav(blob: bytes) -> Dict[str, Any]:
    try:
        from christman_voice_sdk.audio.speech_recognition_engine import (
            SpeechRecognitionEngine,
        )
    except ImportError as exc:
        return {
            "ok": False,
            "text": "",
            "error": f"Christman-Sound package is not on this machine: {exc}",
        }

    try:
        pcm, rate, width = pcm_from_wav(blob)
    except (ValueError, wave.Error) as exc:
        return {"ok": False, "text": "", "error": str(exc)}

    engine = SpeechRecognitionEngine()
    result = engine.recognize_from_bytes(pcm, sample_rate=rate, sample_width=width)
    payload = result.to_dict()
    payload["ok"] = result.is_user_speech
    if not result.is_user_speech:
        payload["text"] = ""
        payload["error"] = result.metadata.get("error") or result.status.value
    else:
        payload["error"] = None
    return payload


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
        print(json.dumps({"ok": False, "text": "", "error": "pass a WAV path"}))
        return 2
    result = hear_file(args[0])
    print(json.dumps(result))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
