import django
import pytest

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient

django.setup()


class BaseTestCase(TestCase):
    client = APIClient()

    test_user = {
        'username': 'test',
        'email': 'test@mail.com',
        'password1': 'testPass1!',
        'password2': 'testPass1!'
    }


@pytest.fixture
def base_test_case():
    yield BaseTestCase
