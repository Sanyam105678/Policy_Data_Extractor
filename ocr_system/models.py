from django.db import models
from decimal import Decimal


class Policy(models.Model):

    # -------------------------
    # 1. Insured Details
    # -------------------------
    insured_name = models.CharField(max_length=255, null=True, blank=True)
    insured_email = models.EmailField(null=True, blank=True)
    insured_mobile = models.CharField(max_length=20, null=True, blank=True)
    insured_address = models.TextField(null=True, blank=True)
    insured_pan = models.CharField(max_length=20, null=True, blank=True)
    insured_aadhaar = models.CharField(max_length=20, null=True, blank=True)

    # -------------------------
    # 2. Policy Details
    # -------------------------
    insurance_company_name = models.CharField(max_length=255, null=True, blank=True)
    policy_sub_type = models.CharField(max_length=255, null=True, blank=True)
    policy_plan = models.CharField(max_length=255, null=True, blank=True)

    # -------------------------
    # 3. Policy Dates
    # -------------------------
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)

    # -------------------------
    # 4. Premium Details (DECIMAL USED)
    # -------------------------
    net_premium = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    gst = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    gross_premium = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    od_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    tp_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    addon_premium = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    pa_count = models.IntegerField(null=True, blank=True)
    pa_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    driver_count = models.IntegerField(null=True, blank=True)
    driver_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    ncb_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    ncb_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    p_ncb = models.CharField(max_length=50, null=True, blank=True)

    premium_without_ncb = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    premium_with_rate = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    discounted_premium = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    premium_discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rate_applied = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True
    )

    # -------------------------
    # 5. Vehicle Details
    # -------------------------
    fuel_type = models.CharField(max_length=50, null=True, blank=True)
    be_fuel_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    body_type = models.CharField(max_length=100, null=True, blank=True)
    variant = models.CharField(max_length=100, null=True, blank=True)
    gvw = models.CharField(max_length=50, null=True, blank=True)
    cubic_capacity = models.CharField(max_length=50, null=True, blank=True)
    seating_capacity = models.CharField(max_length=50, null=True, blank=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    engine_number = models.CharField(max_length=100, null=True, blank=True)
    chassis_number = models.CharField(max_length=100, null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)

    # -------------------------
    # System Fields
    # -------------------------
    raw_pdf = models.FileField(upload_to="pdfs/", null=True, blank=True)
    raw_text = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=50,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Extracted", "Extracted"),
            ("Partial Extraction", "Partial Extraction"),
            ("Needs Review", "Needs Review"),
            ("OCR Failed", "OCR Failed"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    review_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=200, blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.insured_name or "Policy"

    def get_missing_fields(self):
        missing = []
        missing.extend(
            f
            for f in [
                "insured_name",
                "insurance_company_name",
                "start_date",
                "registration_number",
            ]
            if not getattr(self, f)
        )
        return missing



   