from django.core.exceptions import ValidationError


def validate_signup_password(password: str):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters.')
    if password.isdigit():
        raise ValidationError('Password cannot be entirely numeric.')
