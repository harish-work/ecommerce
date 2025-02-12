from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User
from rest_framework.authtoken.models import Token
# Create your tests here.

class TestAccounts(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com',password='password')

    """Testing ACCOUNTS API"""
    def test_register(self):
        """tetsing register api"""
        data = {
            "email": "testing@gmail.com",
            "name": "test",
            "password": "password"
        }
        response = self.client.post(reverse('register'),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_login(self):
        """testing login api"""
        data = {
            "email":"test@gmail.com",
            "password":"password"
        }
        response = self.client.post(reverse('login'),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_userdetails(self):
        """testcase for checking authenticated users"""
        self.token,self.created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('details'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)