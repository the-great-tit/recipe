from rest_framework.exceptions import ValidationError
"""Utitlities for reusability."""


def validation_error(error):
    raise ValidationError({'status': 400, 'error': error})
