import random
import string
import requests
from api.routes import API_BASE_URL  # Импортируем API_BASE_URL из routes.py

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Метод регистрации нового курьера возвращает список из логина, пароля и ID
# Если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    """Метод регистрации нового курьера возвращает список из логина и пароля."""
    # Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    # Создаём список, чтобы метод мог его вернуть
    login_pass = []

    # Генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(f'{API_BASE_URL}/courier', json=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
        return login_pass  # Возвращаем только логин, пароль и имя

    # Выводим сообщение об ошибке, если регистрация не удалась
    print(f"Ошибка регистрации курьера: {response.status_code} - {response.text}")
    return []