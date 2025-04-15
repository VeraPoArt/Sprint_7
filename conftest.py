import pytest
from api.client import ApiClient
from utils.helpers import register_new_courier_and_return_login_password
import requests
from api.routes import API_BASE_URL
import allure
import random

@pytest.fixture(scope="function")
def api_client():
    """Фикстура для создания экземпляра ApiClient."""
    return ApiClient()

@pytest.fixture(scope="function")
def courier(api_client):
    """Фикстура для создания нового курьера и его удаления после завершения теста."""
    # Генерация уникальных данных для курьера
    login = f"login_{random.randint(1000, 9999)}"
    password = "password123"
    first_name = "FirstName"

    # Регистрация нового курьера
    with allure.step("Регистрация нового курьера"):
        response = requests.post(f'{API_BASE_URL}/courier', json={
            "login": login,
            "password": password,
            "firstName": first_name
        })
        if response.status_code == 201:
            print(f"Courier {login} created successfully.")
        else:
            pytest.fail(f"Failed to register courier: {response.text}")

    # Логинимся, чтобы получить ID курьера
    login_payload = {
        "login": login,
        "password": password
    }
    with allure.step(f"Вход курьера с логином {login} для получения ID"):
        response = requests.post(f'{API_BASE_URL}/courier/login', json=login_payload)

        if response.status_code == 200:
            courier_id = response.json().get('id')
            if not courier_id:
                pytest.fail("Не удалось получить ID курьера после логина.")
            
            # Данные, которые будут переданы тесту
            courier_data = {
                "login": login,
                "password": password,
                "firstName": first_name,
                "id": courier_id
            }
            
            # Передаем управление тесту
            yield courier_data
            
            # Выполняется после завершения теста - удаление курьера
            with allure.step(f"Удаление курьера с ID {courier_id}"):
                delete_response = requests.delete(f'{API_BASE_URL}/courier/{courier_id}')
                if delete_response.status_code == 200:
                    print(f"Courier {login} with ID {courier_id} deleted successfully.")
                else:
                    print(f"Warning: Failed to delete courier {login} with ID {courier_id}. Status: {delete_response.status_code}, Response: {delete_response.text}")
        else:
            pytest.fail(f"Не удалось выполнить логин для курьера. Статус: {response.status_code}, Ответ: {response.text}")

@pytest.fixture
def order_data():
    """Фикстура, возвращающая тестовые данные для создания заказа."""
    with allure.step("Подготовка данных заказа"):
        return {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
        }