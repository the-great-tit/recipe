import pytest

register_url = '/api/auth/register/'
login_url = '/api/auth/login/'
new_user = {'username': 'test2', 'email': 'test2@mail.com',
            'password': 'testPass1!'}
existing_user = {'username': 'test', 'email': 'test@mail.com',
                 'password': 'testpass'}
existing_user_with_wrong_password = {'username': 'test',
                                     'email': 'test@mail.com',
                                     'password': 'wrongpass'}


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
    assert post_data.status_code == 200
    assert 'token' in post_data.json()


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
