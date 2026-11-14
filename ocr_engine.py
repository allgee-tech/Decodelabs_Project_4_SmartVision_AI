"""Tesseract OCR helpers for SmartVision AI."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import pytesseract
from pytesseract import Output


DEFAULT_TESSERACT_PATH = Path(r"E:\Program Files\tesseract.exe")


def configure_tesseract() -> str:
    """Configure pytesseract and return the executable path in use.

    SMARTVISION_TESSERACT_CMD can override the usual Windows install path.
    If Tesseract is already available on PATH, that installation is used.
    """
    configured_path = os.environ.get("SMARTVISION_TESSERACT_CMD")
    if configured_path:
        executable = Path(configured_path)
        if not executable.is_file():
            raise FileNotFoundError(
                "SMARTVISION_TESSERACT_CMD points to a missing file: "
                f"{configured_path}"
            )
        pytesseract.pytesseract.tesseract_cmd = str(executable)
        return str(executable)

    if DEFAULT_TESSERACT_PATH.is_file():
        pytesseract.pytesseract.tesseract_cmd = str(DEFAULT_TESSERACT_PATH)
        return str(DEFAULT_TESSERACT_PATH)

    path_executable = shutil.which("tesseract")
    if path_executable:
        pytesseract.pytesseract.tesseract_cmd = path_executable
        return path_executable

    raise FileNotFoundError(
        "Tesseract OCR was not found. Install it or set "
        "SMARTVISION_TESSERACT_CMD to the full path of tesseract.exe."
    )


def recognize_text(
    image: np.ndarray,
    *,
    lang: str = "eng",
    config: str = "--oem 3 --psm 6",
) -> dict[str, Any]:
    """Recognize text and return text, word confidences, and their average.

    Confidence values are the values reported by Tesseract on a 0–100 scale.
    Blank words and Tesseract's -1 non-word entries are excluded from the mean.
    The average is None when there are no valid word confidence values.
    """
    if not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("OCR input must be a non-empty NumPy image array.")

    configure_tesseract()
    try:
        data = pytesseract.image_to_data(
            image, lang=lang, config=config, output_type=Output.DICT
        )
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract could not be started. Check the executable path and "
            "installation."
        ) from exc
    except pytesseract.TesseractError as exc:
        raise RuntimeError(f"Tesseract OCR failed: {exc}") from exc

    words: list[dict[str, str | float]] = []
    valid_confidences: list[float] = []
    for raw_word, raw_confidence in zip(data["text"], data["conf"]):
        word = str(raw_word).strip()
        try:
            confidence = float(raw_confidence)
        except (TypeError, ValueError):
            continue

        if not word or confidence < 0:
            continue
        words.append({"text": word, "confidence": confidence})
        valid_confidences.append(confidence)

    extracted_text = pytesseract.image_to_string(
        image, lang=lang, config=config
    ).strip()
    average_confidence = (
        sum(valid_confidences) / len(valid_confidences)
        if valid_confidences
        else None
    )

    return {
        "text": extracted_text,
        "words": words,
        "average_confidence": average_confidence,
    }
