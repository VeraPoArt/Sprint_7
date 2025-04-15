def assert_response_status(response, expected_status):
    assert response.status_code == expected_status, f'Expected {expected_status}, but got {response.status_code}'

def assert_json_contains(response, key):
    assert key in response.json(), f'Key "{key}" not found in response JSON'