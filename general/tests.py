from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from general.models import Post

class LoginTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)


class TopTests(TestCase):
    def test_top_posts(self):
        client = Client()
        response = client.get('/top/')
        assert response.status_code == 200


class MainPageTests(TestCase):
    def test_mainpage(self):
        client = Client()
        response = client.get('/')
        assert response.status_code == 200


class AllProfilesTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_all_profiles(self):
        client = Client()
        client.login(**self.credentials)
        response = client.get('/profiles/')
        assert response.status_code == 200

