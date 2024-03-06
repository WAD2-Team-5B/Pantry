from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = "newuser"
        self.password = "test_password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    # tests if force login works for the other tests
    def test_force_login(self):
        self.client.force_login(self.user)
        self.assertTrue(self.client.request().context.get("user").is_authenticated)

    # tests if the client can be logged in directly
    def test_login(self):
        self.client.logout()
        self.client.login(username=self.username, password=self.password)
        self.assertTrue(self.client.request().context.get("user").is_authenticated)

    # tests if the client can be logged in with a post request
    def test_login_post(self):
        self.client.logout()
        response = self.client.post(
            reverse("pantry:login"),
            {"username": self.username, "password": self.password},
        )
        self.assertTrue(response.client.request().context.get("user").is_authenticated)

    # tests if the client can be logged out directly
    def test_logout(self):
        self.client.force_login(self.user)
        self.client.logout()
        self.assertTrue(self.client.request().context.get("user").is_anonymous)

    # tests if the client can be logged out with a get request
    def test_logout_get(self):
        self.client.force_login(self.user)
        self.client.get(reverse("pantry:logout"))
        self.assertTrue(self.client.request().context.get("user").is_anonymous)


class TestViewsAuthentication(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    # tests if base.html template shows correct navbar when user is logged in
    def test_base_html_navbar_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        index = self.client.get("/")
        self.assertContains(index, "Logout")
        self.assertContains(index, "Profile")
        self.assertNotContains(index, "Sign Up")
        self.assertNotContains(index, "Login")

    # tests if base.html template shows correct navbar when user is logged out
    def test_base_html_navbar_anonymous(self):
        self.client.logout()
        index = self.client.get("/")
        self.assertContains(index, "Sign Up")
        self.assertContains(index, "Login")
        self.assertNotContains(index, "Logout")
        self.assertNotContains(index, "Profile")