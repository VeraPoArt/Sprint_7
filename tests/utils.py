import requests
import random
import string
from api.routes import API_BASE_URL  # Импортируем API_BASE_URL из routes.py

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{API_BASE_URL}/courier', json=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
        login_pass.append(response.json().get('id'))
        return login_pass

    print(f"Ошибка регистрации курьера: {response.status_code} - {response.text}")
    return []