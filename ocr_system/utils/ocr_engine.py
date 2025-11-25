import os
import uuid
from pdf2image import convert_from_path
import pytesseract
from django.conf import settings


def extract_text_from_pdf(pdf_path):
    """Convert PDF → images → OCR text extraction."""
    ocr_output = []
    errors = []

    # Create log directory
    log_dir = os.path.join(settings.MEDIA_ROOT, "ocr_logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{uuid.uuid4()}.txt")

    try:
        # Convert PDF pages to images (requires POPPLER)
        images = convert_from_path(pdf_path, dpi=300)

        for i, image in enumerate(images):
            try:
                text = pytesseract.image_to_string(image)
                ocr_output.append(text)
            except Exception as e:
                errors.append(f"OCR failed on page {i+1}: {str(e)}")

        # Write full OCR text to log file
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n\n--- PAGE BREAK ---\n\n".join(ocr_output))

        return "\n".join(ocr_output), errors, log_file

    except Exception as e:
        return "", [str(e)], log_file

        