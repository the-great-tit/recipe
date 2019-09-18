import django
import pytest

from django.urls import reverse
from django.core.management import call_command
from rest_framework.test import APITestCase, APIClient

django.setup()


class BaseTestCase(APITestCase):
    client = APIClient()
    login_url = reverse('login')
    existing_user = {'username': 'test',
                     'email': 'test@mail.com',
                     'password': 'testpass'}


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """enable db access for all tests"""
    pass


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test-data.json')


@pytest.fixture
def base_test_case():
    yield BaseTestCase


@pytest.fixture
def post_data(base_test_case, url, data):
    """helper function to test posting data to the specified url """
    return base_test_case.client.post(url, data, format='json')


@pytest.fixture
def signup_user(base_test_case):
    """Signin user when called
    """
    return base_test_case.client.post(base_test_case.login_url,
                                      base_test_case.existing_user)
