"""Streamlit interface for the SmartVision AI OCR application."""

from __future__ import annotations

from typing import Any

import cv2
import pandas as pd
import streamlit as st

from image_processor import load_image, preprocess_image
from ocr_engine import recognize_text


SUPPORTED_IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "tif", "tiff", "webp"]


@st.cache_data(show_spinner=False)
def analyze_uploaded_image(image_bytes: bytes) -> dict[str, Any]:
    """Decode, preprocess, and recognize an uploaded image."""
    original_bgr = load_image(image_bytes)
    grayscale, blurred, thresholded = preprocess_image(original_bgr)
    ocr_result = recognize_text(thresholded)

    return {
        "original_rgb": cv2.cvtColor(original_bgr, cv2.COLOR_BGR2RGB),
        "grayscale": grayscale,
        "blurred": blurred,
        "processed": thresholded,
        "ocr": ocr_result,
    }


def main() -> None:
    """Render the upload, OCR result, confidence, and download interface."""
    st.set_page_config(
        page_title="SmartVision AI | OCR",
        page_icon=":material/document_scanner:",
        layout="wide",
    )
    st.title("SmartVision AI")
    st.markdown(
        "Upload an image containing text. SmartVision AI prepares it with "
        "OpenCV, then uses Tesseract to recognize the text and estimate "
        "word-level confidence."
    )

    with st.sidebar:
        st.header("How it works")
        st.markdown(
            "1. Upload a text image.\n"
            "2. Convert it to grayscale, blur noise, and apply adaptive thresholding.\n"
            "3. Review the recognized text and Tesseract confidence scores."
        )
        st.caption("Supported formats: PNG, JPG, JPEG, BMP, TIFF, and WebP.")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=SUPPORTED_IMAGE_TYPES,
        help="Choose a clear image of printed text for best results.",
    )
    if uploaded_file is None:
        st.info(
            "Upload an image to see the original, preprocessed image, "
            "recognized text, and confidence scores."
        )
        return

    try:
        with st.spinner("Preparing image and recognizing text..."):
            analysis = analyze_uploaded_image(uploaded_file.getvalue())
    except ValueError as exc:
        st.error(str(exc), title="Could not read this image")
        return
    except FileNotFoundError as exc:
        st.error(
            f"{exc}\n\nInstall Tesseract OCR or check its configured path.",
            title="Tesseract OCR is unavailable",
        )
        return
    except RuntimeError as exc:
        st.error(str(exc), title="OCR could not be completed")
        return

    st.header("Image review")
    original_column, processed_column = st.columns(2)
    with original_column:
        st.subheader("Original image")
        st.image(
            analysis["original_rgb"],
            alt="Original uploaded image containing text",
            width="stretch",
        )
    with processed_column:
        st.subheader("Preprocessed image")
        st.image(
            analysis["processed"],
            alt="Grayscale image after blur and adaptive thresholding",
            width="stretch",
        )

    with st.expander("View preprocessing stages"):
        grayscale_column, blur_column = st.columns(2)
        with grayscale_column:
            st.image(
                analysis["grayscale"],
                caption="Grayscale conversion",
                alt="Uploaded image converted to grayscale",
                width="stretch",
            )
        with blur_column:
            st.image(
                analysis["blurred"],
                caption="Gaussian Blur noise reduction",
                alt="Grayscale image after Gaussian Blur",
                width="stretch",
            )

    st.header("Recognition results")
    ocr_result = analysis["ocr"]
    average_confidence = ocr_result["average_confidence"]
    if average_confidence is None:
        st.metric("Average valid word confidence", "Not available")
    else:
        st.metric("Average valid word confidence", f"{average_confidence:.1f}%")
    st.caption(
        "Confidence is Tesseract's estimate for recognized words. It does not "
        "guarantee that the text is correct."
    )

    if ocr_result["text"]:
        st.subheader("Extracted text")
        st.code(ocr_result["text"], language=None)
        st.download_button(
            "Download text file",
            data=ocr_result["text"].encode("utf-8"),
            file_name="smartvision_ocr_result.txt",
            mime="text/plain",
            icon=":material/download:",
        )
    else:
        st.warning("Tesseract did not find readable text in this image.")

    if ocr_result["words"]:
        st.subheader("Word-level confidence")
        confidence_table = pd.DataFrame(ocr_result["words"])
        confidence_table["confidence"] = confidence_table["confidence"].map(
            lambda value: f"{value:.1f}%"
        )
        confidence_table = confidence_table.rename(
            columns={"text": "Word", "confidence": "Confidence"}
        )
        st.dataframe(confidence_table, hide_index=True)
    else:
        st.caption("No valid word confidence scores were returned.")


if __name__ == "__main__":
    main()
