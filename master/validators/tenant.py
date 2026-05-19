import re

from django.core.exceptions import ValidationError

GSTIN_REGEX = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')


def validate_gstin(value: str):
    if not value:
        return
    if not GSTIN_REGEX.match(value.upper()):
        raise ValidationError('Invalid GSTIN format.')
