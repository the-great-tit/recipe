def test_signup(base_test_case):
    response = base_test_case.client.post('/rest-auth/registration/',
                                          base_test_case.test_user,
                                          format='json')
    print(response.data)
    assert response.status_code == 200
