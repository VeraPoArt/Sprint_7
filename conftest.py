import pytest
from api.client import ApiClient
from utils.helpers import register_new_courier_and_return_login_password
import requests
from api.routes import API_BASE_URL
import allure

@pytest.fixture(scope="function")
def api_client():
    """Фикстура для создания экземпляра ApiClient."""
    return ApiClient()

@pytest.fixture(scope="function")
def courier(api_client):
    """Фикстура для создания нового курьера."""
    with allure.step("Регистрация нового курьера"):
        login_pass = register_new_courier_and_return_login_password()
        if not login_pass:
            pytest.fail("Не удалось зарегистрировать нового курьера")

    # Логинимся, чтобы получить ID курьера
    login, password, first_name = login_pass
    login_payload = {
        "login": login,
        "password": password
    }
    
    with allure.step(f"Вход курьера с логином {login} для получения ID"):
        response = requests.post(f'{API_BASE_URL}/courier/login', json=login_payload)

        if response.status_code == 200:
            courier_id = response.json().get('id')
            return {
                "login": login,
                "password": password,
                "firstName": first_name,
                "id": courier_id  # Получаем ID курьера
            }
        else:
            pytest.fail("Не удалось получить ID курьера после логина")

@pytest.fixture(scope="function")
def order_data():
    """Фикстура для данных заказа."""
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]  # Цвет заказа
    }