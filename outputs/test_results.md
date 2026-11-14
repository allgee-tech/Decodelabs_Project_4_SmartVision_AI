# SmartVision AI test results

## Test setup

- Python 3.11.9 in the project's existing virtual environment.
- OpenCV 5.0.0, pytesseract 0.3.13, Tesseract 5.5.3 with English (`eng`) data.
- Each sample was uploaded through Streamlit's headless `AppTest` and processed through the same upload, preprocessing, and OCR path used by the application.
- Character error rate (CER) was calculated against known sample text after removing whitespace and ignoring case. Punctuation was retained. CER is independent of Tesseract's confidence estimate.

## Sample results

| Sample | Description | Average valid word confidence | CER | Notes |
|---|---|---:|---:|---|
| `sample1_printed_document.png` | Clear printed text | 95.0% | 1.0% | Tesseract read `AI` as `Al`. |
| `sample2_receipt.png` | Receipt-style item and amount lines | 93.9% | 0.0% | Text matched the known sample text. |
| `sample3_simulated_uneven_lighting.png` | Generated gradient lighting, slight blur, and light noise | 95.9% | 0.0% | Simulated test image; not a real photograph. |

## Real user image check

A user-provided WhatsApp JPEG photograph of accounting text was processed without saving a copy into the project. It measured 960 × 1280 pixels and ran through grayscale conversion, Gaussian Blur, and adaptive thresholding. Tesseract returned readable portions of the accounting text and an average valid word confidence of 61.3%. No ground-truth transcription was supplied, so character error rate could not be calculated. The lower confidence than the generated samples is consistent with this being a more challenging real-world image; it should be reviewed at higher resolution and with improved lighting or cropping if accuracy is important.

These are results on generated images and should not be treated as a general OCR accuracy estimate.

## Functional checks

- Tesseract executable was found at `E:\Program Files\tesseract.exe`; `eng` language data was available.
- PNG upload, image decode, grayscale conversion, Gaussian Blur, and adaptive thresholding completed.
- The app displayed original and processed images, extracted text, an average confidence metric, and a word-confidence table for each text sample.
- The TXT download button was present for non-empty OCR results. The user confirmed that the browser download and open round trip worked correctly.
- Malformed image bytes produced a friendly image error. A blank image produced an empty-result message and no fabricated confidence value.
- Python compilation and editor diagnostics reported no errors for the application modules.

## Preprocessing comparison

The current Gaussian adaptive-threshold settings (block size 11, constant 2) were compared with 12 variations for each sample: Gaussian and mean adaptive methods, block sizes 15, 21, and 31, and constants 2 and 5. The current configuration tied for the lowest CER on all three samples. Since no alternative improved the measured text accuracy, the implementation was left unchanged.

Compared with OCR on the original, unthresholded images, the processed text was the same for all samples. Average confidence changed from 94.8% to 95.0% for the printed page, from 95.1% to 93.9% for the receipt, and from 95.8% to 95.9% for the simulated lighting sample. This shows preprocessing is integrated, but it does not improve every input or raise confidence in every case.

## Limitations

- The generated samples have known ground truth but do not represent the full range of real photographs, receipts, or documents. The user-provided photograph check did not include ground truth.
- One document sample had a character error despite 95.0% confidence, demonstrating that confidence is not accuracy.
- The download control was verified in Streamlit's headless test; a normal-browser save-and-reopen round trip remains outstanding.
