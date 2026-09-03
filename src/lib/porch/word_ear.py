# ==============================================================================
# © 2025 Everett Nathaniel Christman & Misty Gail Christman
# The Christman AI Project — Luma Cognify AI
# ==============================================================================
"""
Porch word-ear. Reads one WAV. Hands it to SpeechRecognitionEngine.
recognize_from_bytes. Prints RecognitionResult JSON. No cloud. No invented text.

Usage:
  python3 src/lib/porch/word_ear.py /path/to/catch.wav
  python3 src/lib/porch/word_ear.py --stdin   < catch.wav

Needs:
  VOSK_MODEL_PATH pointed at the unzipped model in Downloads
  christman_voice_sdk on PYTHONPATH (Christman-Sound)
"""

from __future__ import annotations

import io
import json
import os
import sys
import wave
from typing import Any, Dict


def _load_engine():
    try:
        from christman_voice_sdk.audio.speech_recognition_engine import (
            SpeechRecognitionEngine,
        )
        from christman_voice_sdk.audio.recognition_result import RecognitionStatus
    except ImportError as exc:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "status": "unavailable",
                    "text": "",
                    "error": (
                        "christman_voice_sdk is not on PYTHONPATH. "
                        f"{exc}"
                    ),
                }
            )
        ) from exc
    return SpeechRecognitionEngine, RecognitionStatus


def _pcm_from_wav(blob: bytes):
    with wave.open(io.BytesIO(blob), "rb") as wf:
        channels = wf.getnchannels()
        width = wf.getsampwidth()
        rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
    if width != 2:
        raise ValueError(f"word-ear wants 16-bit PCM, got sample width {width}")
    if channels == 1:
        pcm = frames
    elif channels == 2:
        pcm = b"".join(frames[i : i + 2] for i in range(0, len(frames), 4))
    else:
        raise ValueError(f"word-ear wants mono or stereo, got {channels} channels")
    return pcm, rate, width


def hear(blob: bytes) -> Dict[str, Any]:
    SpeechRecognitionEngine, RecognitionStatus = _load_engine()
    engine = SpeechRecognitionEngine()
    if not blob:
        return {
            "ok": False,
            "status": "no_speech",
            "text": "",
            "error": "empty_wav",
        }
    try:
        pcm, rate, width = _pcm_from_wav(blob)
    except Exception as exc:
        return {
            "ok": False,
            "status": "error",
            "text": "",
            "error": f"WAV is not readable: {exc}",
        }
    result = engine.recognize_from_bytes(pcm, sample_rate=rate, sample_width=width)
    body = result.to_dict()
    body["ok"] = result.status is RecognitionStatus.OK
    if result.status is RecognitionStatus.OK:
        body["error"] = None
    else:
        body["error"] = result.metadata.get("error") or result.status.value
    return body


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--stdin":
        blob = sys.stdin.buffer.read()
    elif len(argv) >= 2:
        path = argv[1]
        with open(path, "rb") as handle:
            blob = handle.read()
    else:
        sys.stdout.write(
            json.dumps(
                {
                    "ok": False,
                    "status": "error",
                    "text": "",
                    "error": "pass a wav path or --stdin",
                }
            )
            + "\n"
        )
        return 2
    sys.stdout.write(json.dumps(hear(blob)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
