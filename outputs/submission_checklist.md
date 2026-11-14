# DecodeLabs Project 4 submission checklist

## Project files

- [x] Streamlit application: `app.py`
- [x] OpenCV image loading and preprocessing: `image_processor.py`
- [x] Tesseract configuration, OCR, and confidence calculation: `ocr_engine.py`
- [x] Python dependencies: `requirements.txt`
- [x] Setup, usage, limitations, and screenshot references: `README.md`
- [x] Technical project report: `outputs/technical_project_report.md`
- [x] Test measurements and limitations: `outputs/test_results.md`
- [x] Generated document, receipt, and simulated uneven-lighting samples: `samples/`
- [x] Streamlit screenshots: `outputs/screenshots/`
- [x] Git ignore rules for local environments and generated Python cache: `.gitignore`

## Verification completed

- [x] Confirm Tesseract executable and English data are installed.
- [x] Confirm grayscale, Gaussian Blur, and adaptive thresholding execute.
- [x] Confirm actual Tesseract OCR and word confidence values are returned.
- [x] Confirm average valid confidence is computed from reported values only.
- [x] Exercise clear document, receipt-style, and simulated uneven-lighting samples through the Streamlit upload flow.
- [x] Check malformed-image handling and empty OCR output.
- [x] Confirm text download control is shown when OCR text is available.
- [x] Download and open the TXT file in a normal browser session (confirmed by the user).
- [x] Test a user-provided WhatsApp photograph of accounting text and record the result (61.3% mean valid word confidence; no ground truth supplied).

## GitHub preparation

The project files are prepared for version control, but this folder is not currently a Git repository and no remote has been configured. After reviewing the project and deciding which account/repository to use, run these commands from the project directory:

```powershell
git init
git add app.py image_processor.py ocr_engine.py requirements.txt README.md .gitignore samples outputs
git status
git commit -m "Build SmartVision AI OCR application"
```

Then create a repository on GitHub and follow GitHub's instructions to add its remote and push the branch. Do not upload the `venv/` folder. The `.gitignore` excludes it and common local caches.

## Final review before submission

- [x] Supplement the generated uneven-lighting sample with the user-provided real photograph result in `outputs/test_results.md` (the image itself was not copied into the repository).
- [x] Complete the browser TXT save-and-reopen round trip (confirmed by the user).
- [ ] Check that the report, screenshots, and code are included in the selected repository.
- [ ] Review the target programme's submission format and add any requested naming, identity, or presentation details.
