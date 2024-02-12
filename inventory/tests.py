from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Users, Categories, Items, Tags
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class ItemAndCategoryAPITests(APITestCase):
    def setUp(self):
        # Create a test user and get JWT token for authentication
        self.user = Users.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.token = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # URL setup
        self.create_category_url = reverse('create-category')
        self.create_item_url = reverse('create-item')
        self.item_list_url = reverse('item-List')

    def test_create_category(self):
        """
        Ensure we can create a new category.
        """
        data = {"name": "Electronics"}
        response = self.client.post(self.create_category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categories.objects.count(), 1)
        self.assertEqual(Categories.objects.get().name, 'Electronics')

    def test_create_item(self):
        """
        Ensure we can create a new item.
        """
        category = Categories.objects.create(name="Electronics")
        data = {
            "sku": "12345ABC",
            "name": "Smartphone",
            "category": {"name": "Electronics"},  # Assuming nested serialization
            "description": "Latest model",
            "tags": [],  # Assuming no tags for simplicity
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
        self.assertEqual(len(response.data), 1)  # Assuming pagination is set to show 2 items per page
