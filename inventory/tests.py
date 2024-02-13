from os import path
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Categories, Items, Tags
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.management import call_command
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class ItemAndCategoryAPITests(APITestCase):
    def setUp(self):
        # Create a test user and get JWT token for authentication
        # call_command('migrate', interactive=False, verbosity=0)
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }

        # URL setup
        self.live_url = 'http://18.118.147.123:8000/'
        self.create_category_url = self.live_url+'/inventory/category/create'
        self.create_item_url = self.live_url+'/inventory/items/create'
        self.item_list_url = self.live_url+'/inventory/items/'
        self.login_url = self.live_url+'/inventory/users/login'
        self.signup_url = self.live_url+'/inventory/users/signup'
        self.client.post(self.login_url, self.user_data, format='json')
        # category = Categories.objects.get(name='Electronics')

    def test_create_category(self):
        """
        Ensure we can create a new category.
        """
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.token = response.data['tokens']['access'] 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {"name": "Electronics"}
        response = self.client.post(self.create_category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_item(self):
        """
        Ensure we can create a new item.
        """
        category = Categories.objects.create(name="Electronics")
        data = {
            "sku": "12345ABC",
            "name": "Smartphone",
            "category": {"name": "Electronics"},  
            "description": "Latest model",
            "tags": [],  
            "in_stock_quantity": 10,
            "available_stock_quantity": 10,
            "low_stock_threshold": 2
        }
        response = self.client.post(self.create_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Items.objects.count(), 1)
        self.assertEqual(Items.objects.get().name, 'Smartphone')

    def test_item_list(self):
        """
        Ensure we can retrieve a list of items.
        """
        # Setup test data
        category = Categories.objects.create(name="Books")
        item = Items.objects.create(
            sku="BOOK123",
            name="Django for APIs",
            category=category,
            description="Learn Django for building APIs",
            in_stock_quantity=50,
            available_stock_quantity=50,
            low_stock_threshold=5
        )

        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
