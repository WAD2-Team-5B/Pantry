from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.images import ImageFile
from pantry.forms import UserForm
from pantry.models import UserProfile, Recipe, Cuisine, Category, Review, SavedRecipes
from pantry.views import SPACER
from population_script import (
    create_cuisines_and_categories,
    create_recipes,
    create_reviews,
    create_users_and_profiles,
    add_recipe,
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
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        # get a recipe that is created by self.user
        self.user = User.objects.get(username="jeval")
        self.recipe = Recipe.objects.filter(user=self.user)[0]

        # am additional test user must be created, as the population script has users who have already posted reviews
        self.reviewing_user = User.objects.create(username="david", password="123456")

    # tests that review form is not present when a user views their own recipe
    def test_review_form_present_own_recipe(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertNotContains(response, '"post-review-form"')

    # tests that review form is present on other users' recipes
    def test_review_form_present_not_own_recipe(self):
        self.client.force_login(self.reviewing_user)
        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertContains(response, '"post-review-form"')

    # tests that review form is not present when a user has already posted a review
    def test_review_form_present_already_reviewed(self):
        self.client.force_login(User.objects.get(username="andrewH"))
        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )
        self.assertNotContains(response, '"post-review-form"')

    # tests that a posted review is added to the database
    def test_post_review(self):
        self.client.force_login(self.reviewing_user)
        contents = "this is my review :)"
        response = self.client.post(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id]),
            data={"reason": "review", "review": contents},
        )
        review = Review.objects.filter(user=self.reviewing_user)[0]
        self.assertEqual(contents, review.review)

    # tests that the recipe view shows a new review
    def test_post_review_view(self):
        contents = "this is the review that should show up"
        review = Review.objects.create(
            user=self.reviewing_user, review=contents, recipe_id=self.recipe.id
        )

        response = self.client.get(
            reverse(f"pantry:recipe", args=[self.user.id, self.recipe.id])
        )

        self.assertContains(response, contents)

    # tests that the like count is updated in the database when a review is liked
    def test_like_review(self):
        self.client.force_login(self.reviewing_user)

        before_review = Review.objects.get(id=2)

        self.client.post(
            reverse("pantry:like-review"),
            data={"data[reviewId]": before_review.id, "data[like]": "true"},
        )

        after_review = Review.objects.get(id=before_review.id)

        self.assertEqual(before_review.likes + 1, after_review.likes)

    # tests that a like can be taken back
    def test_unlike_review(self):
        self.client.force_login(self.reviewing_user)

        before_review = Review.objects.get(id=2)

        self.client.post(
            reverse("pantry:like-review"),
            data={"data[reviewId]": before_review.id, "data[like]": "true"},
        )

        self.client.post(
            reverse("pantry:like-review"),
            data={"data[reviewId]": before_review.id, "data[like]": "false"},
        )

        after_review = Review.objects.get(id=before_review.id)

        self.assertEqual(before_review.likes, after_review.likes)

    # tests that reviews cannot be liked twice
    """def test_like_review_twice(self):
        self.client.force_login(self.reviewing_user)

        before_review = Review.objects.get(id=2)

        self.client.post(
            reverse("pantry:like-review"),
            data={"data[reviewId]": before_review.id, "data[like]": "true"},
        )
        self.client.post(
            reverse("pantry:like-review"),
            data={"data[reviewId]": before_review.id, "data[like]": "true"},
        )

        after_review = Review.objects.get(id=before_review.id)

        # the like count should have only changed by one despite the request being sent twice
        self.assertEqual(before_review.likes + 1, after_review.likes)"""

    # tests that a newly created recipe is accessible
    def test_new_recipe_view(self):
        recipe = add_recipe(
            {
                "user": User.objects.get(username="andrewS"),
                "cuisine": Cuisine.objects.get(type="Mexican"),
                "categories": Category.objects.filter(type__in=["Low Fat"]),
                "title": "New recipe !!",
                "image": ImageFile(open("./populate_data/vegetarian_tacos.jpeg", "rb")),
                "desc": "Description",
                "ingredients": SPACER.join(["Something", "something else"]),
                "steps": SPACER.join(["Step 1", "Step 2"]),
                "prep": "0:15",
                "cook": "0:10",
                "difficulty": "intermediate",
                "star_count": 25,
                "star_submissions": 6,
            }
        )
        response = self.client.get(
            reverse("pantry:recipe", args=[recipe.user.id, recipe.id])
        )
        self.assertEqual(200, response.status_code)

    # tests that a recipe being saved appears on the page
    def test_save_recipe(self):
        self.client.force_login(self.reviewing_user)
        self.client.post(
            reverse("pantry:recipe", args=[self.recipe.user.id, self.recipe.id]),
            data={"data[bookmarked]": "false"},
        )
        response = self.client.get(
            reverse("pantry:recipe", args=[self.recipe.user.id, self.recipe.id])
        )
        self.assertContains(response, "1 save")

    # tests that saved recipes are stored in the database correctly
    def test_saved_recipe_model(self):
        self.client.force_login(self.reviewing_user)
        self.client.post(
            reverse("pantry:recipe", args=[self.recipe.user.id, self.recipe.id]),
            data={"data[bookmarked]": "false"},
        )
        saved_recipe = SavedRecipes.objects.filter(user=self.reviewing_user)[0]
        self.assertEqual(saved_recipe.recipe, self.recipe)


class TestRecipes(TestCase):
    def setUp(self):
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

    # there should only be one recipe (sushi) on the search page with the query 'sus'
    def test_search_single_item(self):
        response = self.client.get(reverse("pantry:recipes") + "?search_query=sus")

        self.assertContains(response, '<a class="recipe"', count=1)

    # the page should not contain any links to recipes when the search query does not match any
    def test_search_no_items(self):
        response = self.client.get(
            reverse("pantry:recipes") + "?search_query=nothing should match this"
        )

        self.assertNotContains(response, '<a class="recipe"')

    # there should be exactly two recipes (sushi, spaghetti) on the search page with the query 's'
    def test_search_multiple_items(self):
        response = self.client.get(reverse("pantry:recipes") + "?search_query=s")

        self.assertContains(response, '<a class="recipe"', count=2)


class TestCreateARecipe(TestCase):
    def setUp(self):
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        self.user = User.objects.get(username="layla")

    # tests that a posted recipe is added to the database
    def test_create_a_recipe_post(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("pantry:create-a-recipe"),
            data={
                "user": self.user,
                "cuisine": Cuisine.objects.get(type="Italian"),
                "categories": Category.objects.filter(
                    type__in=["Low Fat", "Organic", "Vegetarian"]
                ),
                "name": "New recipe",
                "image": ImageFile(
                    open("./populate_data/spaghetti_carbonara.jpeg", "rb")
                ),
                "description": "Description",
                "ingredients": SPACER.join(["Bacon"]),
                "steps": SPACER.join(["Step 1", "Step 2", "Step 3"]),
                "prep": "0:20",
                "cook": "0:20",
                "difficulty": "intermediate",
                "star_count": 32,
                "star_submissions": 9,
            },
        )

        created_recipe = Recipe.objects.filter(title="New recipe")[0]
        self.assertEqual(created_recipe.user, self.user)


class TestSavedRecipes(TestCase):
    def setUp(self):
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()

        self.user = User.objects.create_user("dave", password="123456")
        self.alt_user = User.objects.get(username="jeval")

        self.recipe = Recipe.objects.get(id=1)

    # tests that the saved recipes page is empty when there are no saved reviews
    def test_no_saved_recipes_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pantry:saved-recipes", args=[self.user.id]))
        self.assertNotContains(response, '<a class="data-card" href="/pantry/recipes/')

    # tests that the saved recipes page is correct when a user saves a recipe
    def test_save_recipe_view_same_user(self):
        self.client.force_login(self.user)

        self.client.post(
            reverse("pantry:recipe", args=[self.recipe.user.id, self.recipe.id]),
            data={"data[bookmarked]": "false"},
        )

        response = self.client.get(reverse("pantry:saved-recipes", args=[self.user.id]))

        self.assertContains(
            response,
            f'<a class="data-card" href="/pantry/recipes/{self.recipe.user.id}/{self.recipe.id}',
        )
        self.assertContains(response, self.recipe.title)

    # tests that the saved recipes page is correct from the perspective of another user
    def test_save_recipe_view_different_user(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("pantry:recipe", args=[self.recipe.user.id, self.recipe.id]),
            data={"data[bookmarked]": "false"},
        )

        self.client.force_login(
            self.alt_user
        )  # log in as a different user to the one who saved the recipe

        response = self.client.get(reverse("pantry:saved-recipes", args=[self.user.id]))

        self.assertContains(response, self.recipe.title)


class TestUserReviews(TestCase):
    def setUp(self):
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        self.user = User.objects.create_user("dave", password="123456")
        self.alt_user = User.objects.get(username="jeval")
        self.recipe = Recipe.objects.get(id=1)

    # tests that the user reviews page is empty when the user has no reviews
    def test_no_user_reviews(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pantry:user-reviews", args=[self.user.id]))

        self.assertNotContains(response, '<a class="data-card" href="/pantry/recipes')

    # tests that the user reivews page is correct
    def test_user_reviews_same_user(self):
        self.client.force_login(self.user)

        review_contents = "hello"
        review = Review.objects.create(
            user=self.user, review=review_contents, recipe_id=self.recipe.id
        )

        response = self.client.get(reverse("pantry:user-reviews", args=[self.user.id]))

        self.assertContains(
            response,
            f'<a class="data-card" href="/pantry/recipes/{self.recipe.user.id}/{self.recipe.id}',
        )
        self.assertContains(response, review_contents)

    # tests that the user reviews page is correct from the perspective of another user
    def test_user_reviews_different_user(self):
        self.client.force_login(self.user)

        review_contents = "hello"
        Review.objects.create(
            user=self.user, review=review_contents, recipe_id=self.recipe.id
        )

        self.client.force_login(self.alt_user)

        response = self.client.get(reverse("pantry:user-reviews", args=[self.user.id]))

        self.assertContains(
            response,
            f'<a class="data-card" href="/pantry/recipes/{self.recipe.user.id}/{self.recipe.id}',
        )
        self.assertContains(response, review_contents)


class TestIndex(TestCase):
    def setUp(self):
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

    # a link to a new recipe should appear on the home page
    def test_new_recipe(self):
        recipe = add_recipe(
            {
                "user": User.objects.get(username="nicole"),
                "cuisine": Cuisine.objects.get(type="Italian"),
                "categories": Category.objects.filter(type__in=["Low Fat"]),
                "title": "Title no other recipe will have",
                "image": ImageFile(open("./populate_data/vegetarian_tacos.jpeg", "rb")),
                "desc": "Description",
                "ingredients": SPACER.join(["Something", "something else"]),
                "steps": SPACER.join(["Step 1", "Step 2"]),
                "prep": "0:15",
                "cook": "0:10",
                "difficulty": "intermediate",
                "star_count": 25,
                "star_submissions": 6,
            }
        )
        response = self.client.get(reverse("pantry:index"))
        self.assertContains(response, f'"/pantry/recipes/{recipe.user.id}/{recipe.id}"')
        self.assertContains(response, recipe.title)


class TestAbout(TestCase):
    # tests that the about page renders the correct template
    def test_about_view(self):
        response = self.client.get(reverse("pantry:about"))
        self.assertTemplateUsed(response, "pantry/about.html")


class TestProfile(TestCase):
    def setUp(self):
        create_users_and_profiles()
        create_cuisines_and_categories()
        create_recipes()
        create_reviews()

        self.user = User.objects.get(username="andrewM")
        self.user_profile = UserProfile.objects.get(user=self.user)

        self.alt_user = User.objects.get(username="jeval")
        self.alt_user_profile = UserProfile.objects.get(user=self.alt_user)

    # tests profile view is correct when viewing own profile
    def test_profile_view_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pantry:user-profile", args=[self.user.id]))

        self.assertContains(response, self.user_profile.bio)

        self.assertContains(response, "Edit Profile")
        self.assertContains(response, "Create A Recipe")
        self.assertContains(response, "My Recipes")
        self.assertContains(response, "My Reviews")
        self.assertContains(response, "Saved Recipes")

    # tests profile view is correct when viewing another user's profile
    def test_profile_view_other_profile(self):
        response = self.client.get(
            reverse("pantry:user-profile", args=[self.alt_user.id])
        )

        self.assertContains(response, self.alt_user.username)
        self.assertContains(response, self.alt_user_profile.bio)

        self.assertContains(response, f"{self.alt_user.username}'s Recipes")
        self.assertContains(response, f"{self.alt_user.username}'s Reviews")
        self.assertContains(response, f"{self.alt_user.username}'s Saved Recipes")

    # tests that the username can be changed
    def test_edit_profile_change_username(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={
                "changed_username": "david",
                "changed_password": "",
                "changed_bio": self.user_profile.bio,
            },
        )
        user = User.objects.get(id=self.user.id)
        self.assertEqual("david", user.username)

    # user should not be able to change their username to one that already exists
    def test_edit_profile_change_username_same(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={
                "changed_username": self.alt_user.username,
                "changed_password": "",
                "changed_bio": self.user_profile.bio,
            },
        )
        user = User.objects.get(id=self.user.id)
        self.assertEqual(self.user.username, user.username)

        self.assertContains(response, "Username already exists!")

    # tests that the bio can be changed
    def test_edit_profile_change_bio(self):
        new_bio = "This is my new bio!!"

        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={
                "changed_username": self.user.username,
                "changed_password": "",
                "changed_bio": new_bio,
            },
        )
        user_profile = UserProfile.objects.get(user=self.user.id)
        self.assertEqual(new_bio, user_profile.bio)

    # tests that the password can be changed (user can then login with new password)
    def test_edit_profile_change_password(self):
        new_password = "This is my new password!!"

        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={
                "changed_username": self.user.username,
                "changed_password": new_password,
                "changed_bio": self.user_profile.bio,
            },
        )

        self.client.logout()

        self.assertTrue(
            self.client.login(username=self.user.username, password=new_password)
        )

    # tests that an account can be deleted
    def test_edit_profile_delete_account(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={"delete-request": "true"},
        )

        self.assertEqual(0, len(User.objects.filter(id=self.user.id)))

    # tests that the user is redirected after their account is deleted
    def test_edit_profile_delete_account_redirect(self):
        self.client.force_login(self.user)
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                "pantry:edit-profile",
            ),
            data={"delete-request": "true"},
        )

        self.assertRedirects(response, reverse("pantry:index"))
