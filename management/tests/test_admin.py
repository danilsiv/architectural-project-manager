from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from management.models import Position


class AdminPositionTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="test_position")

    def test_position_name_should_be_in_search_field(self) -> None:
        """
        Test that position's name is in search_field on position's list page
        :return:
        """
        url = reverse("admin:management_position_changelist")
        response = self.client.get(url)
        self.assertContains(response, "name")
