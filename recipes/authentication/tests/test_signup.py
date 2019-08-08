import pytest

url = '/rest-auth/registration/'
test_user = {
        'username': 'test',
        'email': 'test@mail.com',
        'password1': 'testPass1!',
        'password2': 'testPass1!'
    }


@pytest.mark.parametrize('url, data', [(url, test_user)])
def test_signup_success(post_data):
    assert post_data.status_code == 201


@pytest.mark.parametrize('url, data', [(url, {})])
def test_signup_failure(post_data):
    assert post_data.status_code == 400
