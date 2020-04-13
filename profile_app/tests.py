from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

USERNAME = 'admin'
PASSWORD = 'admin'


class TestProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username=USERNAME,
            password=PASSWORD,
            is_superuser=True
        )
        self.login_text = 'Username'

    def testRequestRootUrl(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        print(response)
        self.assertContains(response, self.login_text)

    def testAuthUrl(self):
        response = self.client.get('/profile/login/')
        self.assertEqual(response.status_code, 200)

    def testAuth(self):
        response = self.client.post(
            '/profile/login/',
            {'username': USERNAME, 'password': PASSWORD}
        )
        self.assertEqual(response.status_code, 200)

    def testLogout(self):
        response = self.client.post(
            '/profile/login/',
            {'username': USERNAME, 'password': PASSWORD}
        )
        response = self.client.get('/profile/logout/')
        self.assertEqual(response.status_code, 302)

    def testLogoutFollowRedirect(self):
        self.client.post(
            '/profile/login/',
            {'username': USERNAME, 'password': PASSWORD}
        )
        response = self.client.get('/profile/logout/', follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
