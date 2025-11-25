import os
import zipfile
import uuid
from django.conf import settings


def save_zip_file(zip_file):
    """Save uploaded ZIP to media/uploads/ folder"""
    zip_name = f"{uuid.uuid4()}.zip"
    upload_path = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_path, exist_ok=True)

    filepath = os.path.join(upload_path, zip_name)

    with open(filepath, "wb+") as dest:
        for chunk in zip_file.chunks():
            dest.write(chunk)

    return filepath


def extract_zip_file(zip_path):
    """Extract ZIP into media/extracted/<unique_id>/ and return PDF file list"""
    extract_id = str(uuid.uuid4())
    extract_dir = os.path.join(settings.MEDIA_ROOT, "extracted", extract_id)
    os.makedirs(extract_dir, exist_ok=True)

    pdf_files = []
    errors = []

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("/"):
                    continue
                if file.lower().endswith(".pdf"):
                    zip_ref.extract(file, extract_dir)
                    pdf_files.append(os.path.join(extract_dir, file))
                else:
                    errors.append(f"Invalid file skipped: {file}")

    except Exception as e:
        errors.append(str(e))

    return pdf_files, errors, extract_dir

    