import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from pytest_redis.factories import redisdb

from recipes.authentication.utils.mails import account_verification

register_url = reverse('register')
login_url = reverse('login')

new_user = {'username': 'test2', 'email': 'test2@mail.com',
            'password': 'testPass1!'}
existing_user = {'username': 'test', 'email': 'test@mail.com',
                 'password': 'testpass'}
existing_user_with_wrong_password = {'username': 'test',
                                     'email': 'test@mail.com',
                                     'password': 'wrongpass'}
token = None
User = get_user_model()


@redisdb
@pytest.mark.parametrize('url, data', [(register_url, new_user)])
def test_register_new_user(post_data):
    assert post_data.status_code == 201
    assert post_data.json() == {'email': 'test2@mail.com',
                                'username': 'test2'}


@pytest.mark.parametrize('url, data', [(register_url, existing_user)])
def test_register_existing_user(post_data):
    assert post_data.status_code == 400
    assert 'user with this email already exists.' in post_data.json()['email']
    assert 'user with this username already exists.' in post_data.json()[
        'username']


@pytest.mark.parametrize('url, data', [(login_url, new_user)])
def test_login_new_user(post_data):
    assert post_data.status_code == 400
    assert post_data.json() == {'error': 'You are not registered'}


@pytest.mark.parametrize('url, data', [(login_url, existing_user)])
def test_login_existing_user(post_data):
    global token
    assert post_data.status_code == 200
    assert 'token' in post_data.json()
    # save token to use when verifying account
    token = post_data.json()['token']


@pytest.mark.parametrize('url, data', [(login_url,
                                        existing_user_with_wrong_password)])
def test_login_existing_user_with_wrong_password(post_data):
    assert post_data.status_code == 400
    assert 'Wrong password or username' in post_data.json()['error']


@pytest.mark.parametrize('url, data', [(login_url, {})])
def test_login_with_empty_data(post_data):
    assert post_data.status_code == 400
    assert 'Please provide a username and password' in post_data.json()[
        'error']


def test_verification_with_wrong_token(base_test_case):
    token = 'bad-token'
    response = base_test_case.client.get(
        f'/api/auth/verify-account/?token={token}/')
    assert response.status_code == 400
    assert 'Invalid token' in response.json()['error']


def test_verification_with_valid_token(base_test_case):
    response = base_test_case.client.get(
        f'/api/auth/verify-account/?token={token}/')
    assert response.status_code == 200
    assert 'Account activated successfully' in response.json()['message']


def test_verification_email_is_sent():
    # confirm that there are no emails in outbox before sending
    assert len(mail.outbox) == 0

    # send email
    account_verification('test@mail.com', token)
    assert len(mail.outbox) == 1
