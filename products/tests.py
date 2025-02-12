from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Category,Product
from django.urls import reverse
# Create your tests here.
class TestProduct(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(type='Test')
        self.products = Product.objects.create(name="testing2",price=100,description="string",category=self.category)

    def test_get_category(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_category(self):
        data = {
            "type":"Test2"
        }
        response = self.client.post(reverse('category-list'),data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_products(self):
        data = {
            "name": "testing",
            "price": 100,
            "description": "string",
            "category": self.category.id
        }
        response = self.client.post(reverse('createproducts-list'),data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        response = self.client.get(reverse('createproducts-list'))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)