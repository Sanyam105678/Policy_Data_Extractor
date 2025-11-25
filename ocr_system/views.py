import os
from django.db.models import Q
from django.conf import settings
from .models import Policy
from .forms import PolicyUploadForm
from .utils.ocr_engine import extract_text_from_pdf
from django.http import FileResponse, Http404
from .utils.zip_handler import save_zip_file, extract_zip_file
from django.shortcuts import render


def upload_policy(request):
    if request.method == "POST":
        form = PolicyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            return _extracted_from_upload_policy(form, request)
    else:
        form = PolicyUploadForm()

    return render(request, "ocr_system/upload.html", {"form": form})


def _extracted_from_upload_policy(form, request):
    insurance_company = form.cleaned_data["insurance_company"]
    zip_file = form.cleaned_data["zip_file"]
    print(insurance_company)

    # Step 1 — Save ZIP
    zip_path = save_zip_file(zip_file)

    # Step 2 — Extract PDFs
    pdf_files, zip_errors, extract_dir = extract_zip_file(zip_path)

    # print("##############Errors - ", zip_errors)

    ocr_results = []

    # Step 3 — OCR Loop
    for pdf in pdf_files:
        raw_text, ocr_errors, log_path = extract_text_from_pdf(pdf)

        # only preview
        preview = f"{raw_text[:500]} ..." if raw_text else "NO TEXT EXTRACTED"

        print(raw_text)
        # temporary placeholder (actual mapping step later)
        policy_obj = Policy()
        policy_obj.raw_text = raw_text  # add new field later if needed
        policy_obj.status = "Extracted"
        policy_obj.save()

        ocr_results.append(
            {
                "pdf": pdf,
                "text": preview,
                "log_file": log_path,
                "errors": ocr_errors,
            }
        )

    context = {
        "pdf_files": pdf_files,
        "zip_errors": zip_errors,
        "ocr_results": ocr_results,
    }

    return render(request, "ocr_system/ocr_result.html", context)




def download_log(request, filename):
    safe_filename = os.path.basename(filename)

    log_dir = os.path.join(settings.MEDIA_ROOT, "ocr_logs")
    file_path = os.path.join(log_dir, safe_filename)

    if not os.path.exists(file_path):
        raise Http404("Log file not found")

    return FileResponse(
        open(file_path, "rb"), as_attachment=True, filename=safe_filename
    )



    