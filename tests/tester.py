import requests
import unittest

class APITests(unittest.TestCase):
    BASE_URL = "http://localhost:5000/api"

    def setUp(self):
        self.token = self.authenticate_user("du1@ua.pt", "du1")
        self.reservation_code = None

    def authenticate_user(self, email, password):
        url = f"{self.BASE_URL}/auth"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()["token"]

    def test_authenticate_user(self):
        url = f"{self.BASE_URL}/auth"
        data = {
            "email": "du1@ua.pt",
            "password": "du1"
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_check_token_validity(self):
        url = f"{self.BASE_URL}/auth/check"
        data = {
            "token": self.token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valid"])

    def test_filter_rooms(self):
        url = f"{self.BASE_URL}/rooms"
        data = {
            "token": self.token,
            "filters": {
                "minSeats": 10,
                "minPowerSockets": 4,
                "type": "Classroom",
                "availableNow": True
            }
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("rooms", response.json())

    def test_get_room_details(self):
         room_id = 1  # Replace with an existing room ID
         url = f"{self.BASE_URL}/rooms/{room_id}"
         data = {
			    "token": self.token
                    }
         response = requests.get(url, json=data)
         self.assertEqual(response.status_code, 200)
         self.assertIn("room", response.json())

    def test_reserve_room(self):
        room_id = 1  # Replace with an existing room ID
        url = f"{self.BASE_URL}/rooms/{room_id}/reserve"
        data = {
            "token": self.token,
            "start_time": 1667856000,
            "duration": 3600,
            "reason": "Meeting"
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json())

    def test_get_equipments(self):
        url = f"{self.BASE_URL}/equipments"
        data = {
            "token": self.token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("equipments", response.json())

    def test_get_equipment_details(self):
        equipment_id = 1  # Replace with an existing equipment ID
        url = f"{self.BASE_URL}/equipments/{equipment_id}"
        data = {
            "token": self.token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("equipment", response.json())

    def test_reserve_equipment(self):
        equipment_id = 1  # Replace with an existing equipment ID
        url = f"{self.BASE_URL}/equipments/{equipment_id}/reserve"
        data = {
            "token": self.token,
            "duration": 3600,
            "reason": "Experiment"
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.reservation_code = response.json()["code"]

    def test_return_equipment(self):
        equipment_id = 1  # Replace with an existing equipment ID
        url = f"{self.BASE_URL}/equipments/{equipment_id}/return"
        data = {
            "token": self.token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_get_user_reservations(self):
        url = f"{self.BASE_URL}/users/reservations"
        data = {
            "token": self.token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("reservations", response.json())

    def test_get_locker_details(self):
        if self.reservation_code is not None:
            url = f"{self.BASE_URL}/locker/{self.reservation_code}"
            data = {
                "token": self.token
            }
            response = requests.post(url, json=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("locker", response.json())

if __name__ == "__main__":
    unittest.main()
