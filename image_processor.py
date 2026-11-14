"""Image loading and preprocessing helpers for SmartVision AI."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def load_image(image_source: bytes | bytearray | str | Path) -> np.ndarray:
    """Load an image from uploaded bytes or a file path as a BGR array.

    Raises:
        ValueError: If the input is empty or OpenCV cannot decode it.
    """
    if isinstance(image_source, (bytes, bytearray)):
        image_bytes = np.frombuffer(image_source, dtype=np.uint8)
    else:
        path = Path(image_source)
        try:
            image_bytes = np.fromfile(path, dtype=np.uint8)
        except OSError as exc:
            raise ValueError(f"Could not read image file: {path}") from exc

    if image_bytes.size == 0:
        raise ValueError("The image is empty or could not be read.")

    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    if image is None or image.size == 0:
        raise ValueError("The file is not a valid, supported image.")

    return image


def preprocess_image(
    image: np.ndarray,
    *,
    blur_kernel_size: int = 5,
    adaptive_block_size: int = 11,
    adaptive_c: int = 2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return grayscale, Gaussian-blurred, and adaptive-threshold images.

    The first two settings that define kernel sizes must be positive odd
    integers. Adaptive thresholding works on a single-channel grayscale image.
    """
    if not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("Image must be a non-empty NumPy array.")
    if image.dtype != np.uint8:
        raise ValueError("Image must use 8-bit unsigned integer pixels.")
    if image.ndim == 2:
        grayscale = image
    elif image.ndim == 3 and image.shape[2] == 3:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.ndim == 3 and image.shape[2] == 4:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        raise ValueError("Image must be grayscale, BGR, or BGRA format.")

    for name, value in (
        ("blur_kernel_size", blur_kernel_size),
        ("adaptive_block_size", adaptive_block_size),
    ):
        if not isinstance(value, int) or value <= 0 or value % 2 == 0:
            raise ValueError(f"{name} must be a positive odd integer.")
    if adaptive_block_size < 3:
        raise ValueError("adaptive_block_size must be at least 3.")

    blurred = cv2.GaussianBlur(
        grayscale, (blur_kernel_size, blur_kernel_size), sigmaX=0
    )
    thresholded = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        adaptive_block_size,
        adaptive_c,
    )
    return grayscale, blurred, thresholded
