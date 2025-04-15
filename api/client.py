import requests
from .routes import API_BASE_URL

class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    def create_courier(self, login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return requests.post(f'{API_BASE_URL}/courier', json=payload)

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{self.base_url}/courier/login', json=payload)
        return response

    def delete_courier(self, courier_id):
        response = requests.delete(f'{self.base_url}/courier/{courier_id}')
        return response

    def create_order(self, order_data):
        response = requests.post(f'{self.base_url}/orders', json=order_data)
        return response

    def finish_order(self, order_id):
        response = requests.put(f'{self.base_url}/orders/finish/{order_id}', json={"id": order_id})
        return response

    def cancel_order(self, track):
        response = requests.put(f'{self.base_url}/orders/cancel', json={"track": track})
        return response

    def get_orders(self):
        response = requests.get(f'{self.base_url}/orders')
        return response

    def get_order_by_track(self, track):
        response = requests.get(f'{self.base_url}/orders/track?t={track}')
        return response

    def accept_order(self, order_id, courier_id):
        response = requests.put(f'{self.base_url}/orders/accept/{order_id}?courierId={courier_id}')
        return response