from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.images import ImageFile
from pantry.forms import UserForm
from pantry.models import UserProfile, Recipe, Cuisine, Category
from pantry.views import SPACER
from population_script import (
    create_cuisines_and_categories,
    create_recipes,
    create_reviews,
    create_users_and_profiles,
)


class TestLogin(TestCase):
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


class TestSignup(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"

        self.existing_user = User.objects.create_user(
            username="existing_user", password=""
        )

    # tests if the signup view is working and has a form on it with inputs
    def test_signup_view_get(self):
        response = self.client.get(reverse("pantry:signup"))

        # check there is a form, with 5 inputs (3 for user form + csrf + submit)
        self.assertContains(response, "<form")
        self.assertContains(response, "<input", count=5)

        # the page contains elements with the correct ids
        self.assertContains(response, 'id="username"')
        self.assertContains(response, 'id="password"')
        self.assertContains(response, 'id="confirm-password"')

    # valid UserForm should have no errors
    def test_user_form_success(self):
        signup_form = UserForm(
            data={
                "username": self.username,
                "password": self.password,
                "confirm_password": self.password,
            }
        )

        # signup form contains no errors
        self.assertEqual(0, len(signup_form.errors))

    # signup should prevent multiple users with the same username
    def test_user_form_user_already_exists(self):
        signup_form = UserForm(
            data={
                "username": self.existing_user.username,
                "password": self.password,
                "confirm_password": self.password,
            }
        )

        # signup form contains one error
        self.assertEqual(1, len(signup_form.errors))

        # check that the error is relevant
        self.assertInHTML(
            "A user with that username already exists.",
            signup_form.errors.get("username")[0],
        )

    # tests a successful signup request
    def test_signup_success(self):
        response = self.client.post(
            reverse("pantry:signup"),
            data={
                "username": self.username,
                "password": self.password,
                "confirm_password": self.password,
            },
        )

        # redirects to index
        self.assertRedirects(response, reverse("pantry:index"))

        # user has been added to the database
        user = User.objects.get(username=self.username)
        self.assertIsNotNone(user)

        # user has a corresponding userprofile created
        user_profile = UserProfile.objects.get(user=user)
        self.assertIsNotNone(user_profile)


class TestBase(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    # tests if base.html template shows correct navbar when user is logged in
    def test_base_html_navbar_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/")
        self.assertContains(response, "Logout")
        self.assertContains(response, self.username)
        self.assertContains(response, self.username)
        self.assertNotContains(response, "Sign Up")
        self.assertNotContains(response, "Login")

    # tests if base.html template shows correct navbar when user is logged out
    def test_base_html_navbar_anonymous(self):
        self.client.logout()
        response = self.client.get("/")
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Login")
        self.assertNotContains(response, "Logout")
        self.assertNotContains(response, "Profile")


class TestRecipe(TestCase):
    def setUp(self):
        # from population script
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        # get a recipe that is created by self.user
        self.user = User.objects.get(username="jeval")
        self.recipe = Recipe.objects.filter(user=self.user)[0]

    # tests that review form is not present when a user views their own recipe
    def test_post_review_own_recipe(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertNotContains(response, '"post-review-form"')

    # tests that review form is present on other users' recipes
    def test_post_review_not_own_recipe(self):
        # a test user must be created, as the population script has users who have already posted reviews
        self.client.force_login(
            User.objects.create(username="david", password="123456")
        )

        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertContains(response, '"post-review-form"')

    # tests that review form is not present when a user has already posted a review
    def test_post_review_already_reviewed(self):
        self.client.force_login(User.objects.get(username="andrewH"))
        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertNotContains(response, '"post-review-form"')


class TestRecipes(TestCase):
    def setUp(self):
        # from population script
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        # get a recipe that is created by self.user
        self.user = User.objects.get(username="jeval")
        self.recipe = Recipe.objects.filter(user=self.user)[0]

    # tests that create a recipe is visible when the user is logged in
    def test_create_a_recipe_authenticated(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pantry:recipes"))
        self.assertInHTML(
            "<a href=" + reverse("pantry:create-a-recipe") + ">Create A Recipe</a>",
            response.content.decode(),
        )

    # tests that create a recipe is not visible when the user is not logged in
    def test_create_a_recipe_anonymous(self):
        self.client.logout()

        response = self.client.get(reverse("pantry:recipes"))
        self.assertNotContains(response, "Create A Recipe")
