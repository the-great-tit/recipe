import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

from recipes.authentication.utils.mails import auth_email

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
expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoy' \
                'LCJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE1NjY4MDA3ODgsImVtY' \
                'WlsIjoidGVzdCJ9.hhTd70ajdSnyaO2xTXkeQvRYBG3V5BZhhrXgoGhQN-E'
User = get_user_model()


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


def test_verification_with_expired_token(base_test_case):
    response = base_test_case.client.get(
        f'/api/auth/verify-account/?token={expired_token}/')
    assert response.status_code == 400
    assert 'JWT expired' in response.json()['error']


def test_verification_with_valid_token(base_test_case):
    response = base_test_case.client.get(
        f'/api/auth/verify-account/?token={token}/')
    assert response.status_code == 200
    assert 'Account activated successfully' in response.json()['message']


def test_auth_email_is_sent():
    # confirm that there are no emails in outbox before sending
    assert len(mail.outbox) == 0

    # send email
    auth_email('test@mail.com', 'test', 'mail_templates/verify_account.html',
               token)
    assert len(mail.outbox) == 1


def test_reset_password_request(base_test_case):
    # an error should be returned if no email is provided
    response = base_test_case.client.post('/api/auth/reset-password/')
    assert response.status_code == 400
    assert 'Please provide an email' in response.json()['error']

    # an error should be returned if the email format is invalid
    response = base_test_case.client.post(
        '/api/auth/reset-password/',
        {"email": "bad-email"}
    )
    assert response.status_code == 400
    assert 'Invalid email format' in response.json()['error']

    # an error should be returned if an unregistered email is provided
    response = base_test_case.client.post(
        '/api/auth/reset-password/',
        {"email": "bad-email@mail.com"}
    )
    assert response.status_code == 400
    assert 'That email is not registered' in response.json()['error']

    # should be successful if a registered email is provided
    response = base_test_case.client.post(
        '/api/auth/reset-password/',
        {"email": "test@mail.com"}
    )
    assert response.status_code == 200
    assert 'Reset password email sent' in response.json()['message']


def test_reset_password_page(base_test_case):
    # an error should be returned if an expired token is used
    response = base_test_case.client.get(
        f'/api/auth/reset-password/?token={expired_token}',
    )
    assert response.status_code == 400
    assert 'JWT expired' in response.json()['error']

    # an error should be returned if an invalid token is used
    response = base_test_case.client.get(
        '/api/auth/reset-password/?token=bad_token',
    )
    assert response.status_code == 400
    assert 'Invalid token' in response.json()['error']

    # an error should be returned if token is not in url
    response = base_test_case.client.get(
        '/api/auth/reset-password/',
    )
    assert response.status_code == 400
    assert 'Invalid url. Token parameter is required' in response.json()[
        'error']

    # success
    response = base_test_case.client.get(
        f'/api/auth/reset-password/?token={token}',
    )
    assert response.status_code == 200
    assert 'You can now enter your new password' in response.json()['message']


def test_reset_password_confirm(base_test_case):
    # an error should be returned if an expired token is used
    response = base_test_case.client.put(
        f'/api/auth/reset-password/?token={expired_token}',
        {"password": "test-password"}
    )
    assert response.status_code == 400
    assert 'JWT expired' in response.json()['error']

    # an error should be returned if an invalid token is used
    response = base_test_case.client.put(
        '/api/auth/reset-password/?token=bad_token',
        {"password": "test-password"}
    )
    assert response.status_code == 400
    assert 'Invalid token' in response.json()['error']

    # an error should be returned if token is not in url
    response = base_test_case.client.put(
        '/api/auth/reset-password/',
        {"password": "test-password"}
    )
    assert response.status_code == 400
    assert 'Invalid url. Token parameter is required' in response.json()[
        'error']

    # an error should be returned if no password is provided
    response = base_test_case.client.put(
        f'/api/auth/reset-password/?token={token}',
    )
    assert response.status_code == 400
    assert 'Please enter your new password' in response.json()['error']

    # an error should be returned if password is too short
    response = base_test_case.client.put(
        f'/api/auth/reset-password/?token={token}',
        {"password": "test"}
    )
    assert response.status_code == 400
    assert 'Password has to be at least 8 characters long' in response.json()[
        'error']

    # success
    response = base_test_case.client.put(
        f'/api/auth/reset-password/?token={token}',
        {"password": "test-password"}
    )
    assert response.status_code == 200
    assert 'Password reset successfully' in response.json()['message']
