import pytest
import requests
import allure

from utils.assertions import assert_response_status, assert_json_contains
from api.routes import API_BASE_URL

@allure.epic("API Testing")
@allure.feature("Order Management")
class TestOrders:
    @allure.title("Тест на успешное создание заказа")
    def test_create_order_success(self):
        """Проверка успешного создания заказа."""
        payload = {
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
        
        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f'{API_BASE_URL}/orders', json=payload)
        
        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 201  # Код 201 для успешного создания
            assert "track" in response.json()  # Проверяем, что в ответе есть track
        
        self.order_id = response.json()["track"]  # Сохраняем трекинговый номер в атрибуте класса

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Тест на создание заказа с разными цветами")
    def test_create_order_with_colors(self, api_client, order_data, color):
        """Проверка, что можно указать один из цветов, оба цвета или не указывать цвет."""
        order_data['color'] = color
        
        with allure.step(f"Отправка запроса на создание заказа с цветами: {color}"):
            response = api_client.create_order(order_data)
        
        with allure.step("Проверка успешного ответа на создание заказа"):
            assert_response_status(response, 201)
            assert_json_contains(response, 'track')

    @allure.title("Проверка получения списка заказов")
    def test_get_orders_success(self, api_client):
        """Проверка, что в тело ответа возвращается список заказов."""
        with allure.step("Отправка запроса на получение списка заказов"):
            response = api_client.get_orders()
        
        with allure.step("Проверка успешного ответа на получение списка заказов"):
            assert_response_status(response, 200)
            assert_json_contains(response, 'orders')

    @allure.title("Проверка создания заказа с отсутствующими полями")
    def test_create_order_missing_fields(self, api_client):
        """Проверка, что запрос без обязательных полей возвращает ошибку."""
        with allure.step("Отправка запроса с отсутствующими обязательными полями"):
            response = api_client.create_order({
                "firstName": "",
                "lastName": "",
                "address": "",
                "metroStation": "",
                "phone": "",
                "rentTime": 0,
                "deliveryDate": "",
                "comment": ""
            })
        
        with allure.step("Проверка ответа на запрос с отсутствующими полями"):
            assert_response_status(response, 500)

@allure.feature("Order Acceptance")
class TestAcceptOrder:
    def create_order_and_accept(self, api_client, courier, order_payload):
        """Утилита для создания и принятия заказа, возвращает order_id и response."""
        with allure.step("Создание заказа"):
            order_response = requests.post(f'{API_BASE_URL}/orders', json=order_payload)
            assert order_response.status_code == 201  # Код 201 для успешного создания
            order_id = order_response.json()["track"]  # Получаем order_id (или track)

        with allure.step("Принятие заказа курьером"):
            accept_url = f"{API_BASE_URL}/v1/orders/accept/{order_id}?courierId={courier['id']}"
            accept_response = requests.put(accept_url)  # Используем PUT запрос
        
        return order_id, accept_response

    @allure.title("Проверка, что запрос без ID курьера возвращает ошибку")
    def test_accept_order_missing_courier_id(self, api_client):
        """Проверка, что запрос без id курьера возвращает ошибку."""
        order_id = "1"
        with allure.step(f"Отправка запроса с отсутствующим ID курьера для заказа {order_id}"):
            response = api_client.accept_order(order_id, "")
        
        with allure.step("Проверка ответа на запрос без ID курьера"):
            assert response.status_code == 400

    @allure.title("Проверка, что запрос с неверным ID курьера возвращает ошибку")
    def test_accept_order_invalid_courier_id(self, api_client):
        """Проверка, что запрос с неверным id курьера возвращает ошибку."""
        order_id = "1"
        with allure.step(f"Отправка запроса с неверным ID курьера {order_id}"):
            response = api_client.accept_order(order_id, "99999")  # Неверный ID курьера
        
        with allure.step("Проверка ответа на запрос с неверным ID курьера"):
            assert response.status_code == 404

    @allure.title("Проверка, что запрос без ID заказа возвращает ошибку")
    def test_accept_order_missing_order_id(self, api_client, courier):
        """Проверка, что запрос без id заказа возвращает ошибку."""
        with allure.step("Отправка запроса с отсутствующим ID заказа"):
            response = api_client.accept_order("", courier['id'])
        
        with allure.step("Проверка ответа на запрос без ID заказа"):
            assert response.status_code == 404

    @allure.title("Проверка, что запрос с неверным ID заказа возвращает ошибку")
    def test_accept_order_invalid_order_id(self, api_client, courier):
        """Проверка, что запрос с неверным id заказа возвращает ошибку."""
        with allure.step("Отправка запроса с неверным ID заказа"):
            response = api_client.accept_order("99999", courier['id'])  # Неверный ID заказа
        
        with allure.step("Проверка ответа на запрос с неверным ID заказа"):
            assert response.status_code == 404

@allure.feature("Get Order by ID")
class TestGetOrderById:
    @allure.title("Проверка, что запрос без номера заказа возвращает ошибку")
    def test_get_order_missing_id(self, api_client):
        """Проверка, что запрос без номера заказа возвращает ошибку."""
        with allure.step("Отправка запроса без номера заказа"):
            response = requests.get(f'{API_BASE_URL}/orders/track?t=')
        
        with allure.step("Проверка ответа на запрос без номера заказа"):
            assert response.status_code == 400  # Код 400 для неверного запроса

    @allure.title("Проверка, что запрос с несуществующим номером заказа возвращает ошибку")
    def test_get_order_nonexistent_id(self, api_client):
        """Проверка, что запрос с несуществующим номером заказа возвращает ошибку."""
        with allure.step("Отправка запроса с несуществующим номером заказа"):
            response = requests.get(f'{API_BASE_URL}/orders/track?t=99999')  # Неверный ID заказа
        
        with allure.step("Проверка ответа на запрос с несуществующим номером заказа"):
            assert response.status_code == 404  # Код 404 для несуществующего ресур
