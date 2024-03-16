from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.images import ImageFile
from pantry.forms import UserForm
from pantry.models import UserProfile, Recipe, Cuisine, Category
from pantry.views import SPACER
from population_script import add_cuisine, add_recipe


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
        signup = self.client.get(reverse("pantry:signup"))

        # check there is a form, with 5 inputs (3 for user form + csrf + submit)
        self.assertContains(signup, "<form")
        self.assertContains(signup, "<input", count=5)

        # the page contains elements with the correct ids
        self.assertContains(signup, 'id="username"')
        self.assertContains(signup, 'id="password"')
        self.assertContains(signup, 'id="confirm-password"')

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
        self.assertContains(index, self.username)
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


class TestRecipe(TestCase):
    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.alt_username = "other"
        self.alt_user = User.objects.create_user(
            username=self.alt_username, password=self.password
        )
        self.cuisine = add_cuisine("Italian")
        self.recipe = add_recipe(
            {
                "user": self.user,
                "cuisine": self.cuisine,
                "categories": Category.objects.filter(
                    type__in=["Low Fat", "Organic", "Vegetarian"]
                ),
                "title": "Spaghetti Carbonara",
                "image": ImageFile(
                    open("./populate_data/spaghetti_carbonara.jpeg", "rb")
                ),
                "desc": "Classic Italian pasta dish with eggs, cheese, bacon, and black pepper.",
                "ingredients": SPACER.join(
                    ["Pasta", "Eggs", "Parmesan Cheese", "Bacon"]
                ),
                "steps": SPACER.join(
                    [
                        "Boil pasta",
                        "Cook bacon",
                        "Mix eggs and cheese",
                        "Combine all with pasta",
                    ]
                ),
                "prep": "0:20",
                "cook": "0:20",
                "difficulty": "intermediate",
                "saves": 10,
                "star_count": 32,
                "star_submissions": 9,
            }
        )

    def test_recipe_html_authenticated(self):
        self.client.force_login(self.user)
        recipe = self.client.get(f"/pantry/recipes/{self.user.id}/{self.recipe.id}")
        print(recipe.content)
        self.assertContains(recipe, '<button class="review-heart">')

    def test_recipe_html_authenticated_not_own_profile(self):
        self.client.logout()
        self.client.login(username=self.alt_username, passwrd=self.password)
        recipe = self.client.get(f"/pantry/recipes/{self.user.id}/{self.recipe.id}")
        self.assertContains(recipe, '<div class="user-review">')
