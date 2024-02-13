from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.jwt_create_url = reverse('jwt_create')
        self.jwt_refresh_url = reverse('token_refresh')
        self.jwt_verify_url = reverse('token_verify')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'username': 'testuser',
            # 'date_of_birth': '2000-01-01'
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('User Created Successfully', response.data['message'])

    def test_user_login(self):
        self.client.post(self.signup_url, self.user_data, format='json')

        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_jwt_create(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertIn('tokens', login_response.data)

        token = login_response.data['tokens']['access']
        verify_response = self.client.post(self.jwt_verify_url, {'token': token}, format='json')
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    def test_jwt_refresh(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        refresh_token = login_response.data['tokens']['refresh']

        refresh_response = self.client.post(self.jwt_refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
