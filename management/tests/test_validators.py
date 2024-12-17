from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now
from datetime import datetime
from datetime import date

from management.validators import validate_future_date


class ValidateFutureDateTests(TestCase):
    @staticmethod
    def convert_str_to_date_obj(date_string: str) -> date:
        return datetime.strptime(date_string, "%Y-%m-%d").date()

    def test_future_date(self) -> None:
        past_date = "2000-12-12"
        self.assertRaises(
            ValidationError,
            validate_future_date,
            self.convert_str_to_date_obj(past_date)
        )

    def test_past_date(self) -> None:
        future_date = "2040-12-12"
        try:
            validate_future_date(self.convert_str_to_date_obj(future_date))
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly!")

    def test_current_date(self) -> None:
        current_date = now().date()
        try:
            validate_future_date(current_date)
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly!")
