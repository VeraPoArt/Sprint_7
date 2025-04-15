import pytest
import random
import requests
import allure
from utils.assertions import assert_response_status, assert_json_contains
from api.routes import API_BASE_URL

@allure.epic("API Testing")
@allure.feature("Courier Management")
class TestCourier:
    @allure.title("Тест на успешное создание курьера")
    def test_create_courier_success(self, api_client):
        """Проверка успешного создания курьера."""
        # Генерируем уникальные данные для курьера
        unique_login = f"login_{random.randint(1000, 100000)}"
        with allure.step(f"Отправка запроса на создание курьера с логином {unique_login}"):
            response = api_client.create_courier(unique_login, "password123", "FirstName")
        
        with allure.step("Проверка успешного ответа на создание курьера"):
            assert_response_status(response, 201)  # Код 201 для успешного создания
            assert response.json() == {"ok": True}

    @allure.title("Тест на создание дублирующегося курьера")
    def test_create_duplicate_courier(self, api_client, courier):
        """Проверка, что нельзя создать двух одинаковых курьеров."""
        with allure.step(f"Отправка запроса на создание курьера с логином {courier['login']}"):
            response = api_client.create_courier(courier['login'], courier['password'], courier['firstName'])
        
        with allure.step("Проверка ответа на попытку создания дублирующегося курьера"):
            assert_response_status(response, 409)  # Код 409 для конфликта
            assert_json_contains(response, 'message')  # Проверяем, что есть поле с сообщением
            assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."  # Проверяем текст сообщения

    @allure.title("Тест на создание курьера с отсутствующими обязательными полями")
    def test_create_courier_missing_fields(self, api_client):
        """Проверка, что запрос без обязательных полей возвращает ошибку."""
        with allure.step("Отправка запроса с отсутствующими полями"):
            response = api_client.create_courier("", "", "")
        
        with allure.step("Проверка ответа на попытку создания курьера без обязательных полей"):
            assert_response_status(response, 400)  # Код 400 для неверного запроса
            assert_json_contains(response, 'message')  # Проверяем, что есть поле с сообщением
            assert response.json()['message'] == "Недостаточно данных для создания учетной записи"  # Проверяем текст сообщения

    @allure.title("Тест на успешный ответ при регистрации нового курьера")
    def test_create_courier_success_response(self, api_client):
        """Проверка успешного ответа при регистрации нового курьера."""
        unique_login = f"login_{random.randint(1000, 9999)}"
        with allure.step(f"Отправка запроса на создание курьера с логином {unique_login}"):
            response = api_client.create_courier(unique_login, "password123", "FirstName")
        
        with allure.step("Проверка успешного ответа на создание курьера"):
            assert_response_status(response, 201)  # Код 201 для успешного создания
            assert response.json() == {"ok": True}

    @allure.title("Тест на успешный логин курьера")
    def test_login_courier_success(self, api_client, courier):
        """Проверка, что курьер может авторизоваться."""
        with allure.step(f"Логин курьера с логином {courier['login']}"):
            response = api_client.login_courier(courier['login'], courier['password'])
        
        with allure.step("Проверка успешного логина курьера"):
            assert_response_status(response, 200)
            assert_json_contains(response, 'id')

    @allure.title("Тест на логин курьера с отсутствующими полями")
    def test_login_courier_missing_fields(self, api_client):
        """Проверка, что запрос без логина или пароля возвращает ошибку."""
        with allure.step("Отправка запроса с отсутствующими логином или паролем"):
            response = api_client.login_courier("", "")
        
        with allure.step("Проверка ответа на запрос с отсутствующими полями"):
            assert_response_status(response, 400)
            assert_json_contains(response, 'message')
            assert response.json()['message'] == "Недостаточно данных для входа"


    @allure.title("Тест на логин курьера с неверными данными")
    def test_login_courier_invalid_credentials(self, api_client):
        """Проверка, что система вернет ошибку, если логин или пароль неверные."""
        with allure.step("Отправка запроса с неверным логином и паролем"):
            response = api_client.login_courier("invalid_login", "invalid_password")
        
        with allure.step("Проверка ответа на запрос с неверными данными"):
            assert_response_status(response, 404)
            assert_json_contains(response, 'message')
            assert response.json()['message'] == "Учетная запись не найдена"


    @allure.title("Тест на удаление несуществующего курьера")
    def test_delete_courier_nonexistent_id(self, api_client):
        """Проверка, что запрос с несуществующим id курьера возвращает ошибку."""
        with allure.step("Отправка запроса на удаление несуществующего курьера с ID 99999"):
            response = api_client.delete_courier("99999")  # Пытаемся удалить несуществующий ID
        
        with allure.step("Проверка ответа на попытку удаления несуществующего курьера"):
            assert_response_status(response, 404)  # Код 404 для не найдено
            assert_json_contains(response, 'message')  # Проверяем, что есть поле с сообщением
            assert response.json()['message'] == "Курьера с таким id нет."  # Проверяем текст сообщения

    @allure.title("Тест на успешное удаление курьера")
    def test_delete_courier_success(self, api_client, courier):
        """Проверка успешного удаления курьера."""
        with allure.step(f"Отправка запроса на удаление курьера с ID {courier['id']}"):
            response = api_client.delete_courier(courier['id'])
        
        with allure.step("Проверка успешного удаления курьера"):
            assert_response_status(response, 200)
            assert response.json() == {"ok": True}

    @allure.title("Тест на удаление курьера с отсутствующим ID")
    def test_delete_courier_missing_id(self, api_client):
        """Проверка, что запрос без id возвращает ошибку."""
        with allure.step("Отправка запроса на удаление курьера с отсутствующим ID"):
            response = api_client.delete_courier("")
        
        with allure.step("Проверка ответа на запрос с отсутствующим ID"):
            assert_response_status(response, 404)
            assert_json_contains(response, 'message')
            assert response.json()['message'] == "Not Found."

