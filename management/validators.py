from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_future_date(value: str) -> None:
    if value < now().date():
        raise ValidationError("Deadline cannot be in the past")
