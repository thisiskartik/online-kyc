from uuid import uuid4
from django.db import models

INCOME_RANGE_CHOICES = (
    ('<5', 'Up to \u20B95 lac'),
    ('5-10', '\u20B95 - \u20B910 lac'),
    ('10-20', '\u20B910 - \u20B920 lac'),
    ('20-50', '\u20B920 - \u20B950 lac'),
    ('50-100', '\u20B950 - \u20B91 crore'),
    ('>100', 'Over \u20B91 crore')
)


class Identity(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    full_name = models.CharField(max_length=200, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    address = models.TextField()
    income_range = models.CharField(max_length=200, choices=INCOME_RANGE_CHOICES, null=False, blank=False)
    type_of_employment = models.CharField(max_length=200, null=False, blank=False)

    aadhar_number = models.CharField(max_length=200, null=True, blank=True)
    pan_number = models.CharField(max_length=200, null=True, blank=True)

    aadhar_image = models.URLField(max_length=500, null=True, blank=True)
    pan_image = models.URLField(max_length=500, null=True, blank=True)
    face_image = models.URLField(max_length=500, null=True, blank=True)
    signature_image = models.URLField(max_length=500, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.full_name} | {self.date_of_birth}"
