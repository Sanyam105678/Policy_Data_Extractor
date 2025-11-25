from django import forms
from .models import Policy

INSURANCE_CHOICES = [
    ("lic", "LIC"),
    ("icici", "ICICI Lombard"),
    ("tata", "TATA AIG"),
    ("bajaj", "Bajaj Allianz"),
]


class PolicyUploadForm(forms.Form):
    insurance_company = forms.ChoiceField(choices=INSURANCE_CHOICES)
    zip_file = forms.FileField()

    def clean_zip_file(self):
        file = self.cleaned_data.get("zip_file")

        if not file:
            raise forms.ValidationError("Please upload a ZIP file.")

        # Extension check
        if not file.name.lower().endswith(".zip"):
            raise forms.ValidationError("Only .zip files are allowed.")

        # Optional: MIME type check (more strict)
        if file.content_type not in ["application/zip", "application/x-zip-compressed"]:
            raise forms.ValidationError(
                "Invalid file type. Please upload a valid ZIP file."
            )

        return file



   