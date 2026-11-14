# SmartVision AI — Technical Project Report

## 1. Introduction

SmartVision AI is an image-based Optical Character Recognition (OCR) application developed for the DecodeLabs Artificial Intelligence Industrial Training Programme, Project 4, Batch 2026. The application uses OpenCV to prepare uploaded images and Tesseract OCR to recognize text.

## 2. Problem statement

Text contained in an image cannot be searched or edited as ordinary text. Manual transcription takes time and can introduce mistakes. SmartVision AI provides a small local application that extracts text from supported image formats and gives users a visual way to review the input, preprocessing, and OCR confidence.

## 3. Objectives

- Accept and validate user-supplied text images.
- Demonstrate grayscale conversion, Gaussian Blur, and adaptive thresholding.
- Perform actual OCR with Tesseract through `pytesseract`.
- Return recognized text and word-level confidence values.
- Calculate the average of valid OCR confidence values without altering them.
- Display the original and processed image and allow the OCR text to be downloaded.
- Handle invalid images, missing Tesseract, and empty OCR output gracefully.

## 4. Technologies used

| Technology | Role |
|---|---|
| Python 3.11 | Application language |
| Streamlit | Upload interface and result display |
| OpenCV | Image decoding and preprocessing |
| Tesseract OCR | Text recognition and confidence estimates |
| `pytesseract` | Python interface to the Tesseract executable |
| NumPy | Image arrays and pixel operations |
| pandas | Word-confidence table in the interface |

## 5. System architecture

1. `app.py` receives an upload, calls image preprocessing and OCR, and presents results.
2. `image_processor.py` decodes the image, validates its pixel data, and returns grayscale, blurred, and thresholded arrays.
3. `ocr_engine.py` finds/configures Tesseract, extracts text and word confidence values, and calculates the valid-confidence average.

```text
Image upload
    ↓
image_processor.load_image
    ↓
grayscale → Gaussian Blur → adaptive threshold
    ↓
ocr_engine.recognize_text
    ↓
text + word confidence + average valid confidence
    ↓
Streamlit results, image previews, and TXT download
```

## 6. Image preprocessing methodology

The image is decoded into an OpenCV BGR array. The processor converts it to grayscale, reducing each pixel to a brightness value. A 5-by-5 Gaussian Blur reduces small variations and noise. Gaussian adaptive thresholding then classifies each pixel as black or white using a local neighborhood, which can help when brightness varies across the image.

The current adaptive-threshold block size is 11 and the subtraction constant is 2. The original, grayscale, blurred, and thresholded arrays are retained so the interface can display the stages. The original image is shown separately from the thresholded image.

## 7. OCR implementation

`ocr_engine.py` configures `pytesseract` to use `E:\Program Files\tesseract.exe` by default, supports the `SMARTVISION_TESSERACT_CMD` environment variable, and falls back to searching PATH. OCR uses English and the Tesseract configuration `--oem 3 --psm 6`.

The engine calls `pytesseract.image_to_data()` to obtain word-level confidence values. Blank entries and Tesseract's negative `-1` non-word values are excluded. The average is the arithmetic mean of the remaining scores. If there are no valid scores, the average is unavailable. The app does not manufacture or increase confidence values.

## 8. Testing and evaluation

The application was exercised with three generated images: a printed document, a receipt-style image, and a simulated uneven-lighting image. The end-to-end Streamlit checks verified image display, recognized text, confidence display, word-level data, and the TXT download control. Invalid image data and a blank image were also checked. A separate user-provided WhatsApp photograph of accounting text was processed in the project's virtual environment; the original image was not copied into the repository.

Character error rate was computed independently against known sample text after removing whitespace and ignoring case. The current thresholding configuration was compared with 12 Gaussian/mean adaptive-threshold parameter variations on each sample.

## 9. Results and discussion

| Sample | Average confidence | CER |
|---|---:|---:|
| Printed document | 95.0% | 1.0% |
| Receipt-style image | 93.9% | 0.0% |
| Simulated uneven lighting | 95.9% | 0.0% |

All three generated samples exceeded the project target of 80% average valid OCR confidence. The printed-document sample contained an `AI` to `Al` recognition error despite 95.0% confidence. This confirms that confidence estimates are not a substitute for ground-truth comparison. No tested threshold variation improved CER, so the existing preprocessing settings were retained. Detailed measurements and limitations are recorded in [test_results.md](./test_results.md).

The real user-provided photograph returned readable portions of the accounting text at 61.3% average valid word confidence. A ground-truth transcription was not available, so text accuracy could not be measured for that image. The lower score illustrates the challenge of real-world image conditions and does not meet the 80% target. The user confirmed that downloading and opening the TXT result in a normal browser worked correctly.

## 10. Conclusion and recommendations

SmartVision AI provides a working local pipeline from image upload through OpenCV preprocessing and Tesseract OCR to a text download control. It displays actual word confidence and handles invalid and empty inputs. The generated test set achieved confidence above 80%, with low character error against its ground truth. The one real photograph check scored 61.3%, with no ground truth available.

For stronger evidence, test with real photographs, scans, and receipts; verify downloaded files in a browser; and compare results against manually checked text. Future work can add rotation correction, deskewing, user-selectable preprocessing, and automated regression tests.
