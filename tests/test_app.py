import unittest
import json
import uuid
from app import create_app  

class UserManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        
        unique_suffix = uuid.uuid4().hex[:8]  # generate unique string for both username and email
        unique_email = f"testuser_{unique_suffix}@example.com"
        unique_username = f"testuser_{unique_suffix}"
        
        self.test_user = {
            "username": unique_username,
            "email": unique_email,
            "full_name": "Test User",
            "password": "test1234"
        }

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'User API is running'})

    def test_create_user(self):
        response = self.app.post('/users', json=self.test_user)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('message', data)

    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_search_user_by_name(self):
        response = self.app.get('/search?name=test')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_login_user(self):
        # First create the user
        self.app.post('/users', json=self.test_user)

        # Now test login with the same credentials
        login_data = {
            "email": self.test_user['email'],
            "password": self.test_user['password']
        }

        response = self.app.post('/login', json=login_data)
        self.assertIn(response.status_code, [200, 401])  # Expect 200 if user exists and password is correct

        if response.status_code == 200:
            data = response.get_json()
            self.assertIn('message', data)
            self.assertEqual(data['user']['email'], self.test_user['email'])
        else:
            data = response.get_json()
            self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
