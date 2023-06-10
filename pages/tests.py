from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from pages.models import Case
from accounts.models import CustomUser


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")
        self.assertContains(response, "<title>Home page</title>")


class AboutpageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            "Mustafa," "mustafa@dev.io", "some_pass"
        )

    def test_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 302)

    def test_about_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")
        self.assertContains(response, "<h1>About page</h1>")


class CasepageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            "Mustafa," "mustafa@dev.io", "some_pass"
        )
        cls.case = Case.objects.create(case_name="Test Case")

    def test_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/cases/")
        self.assertEqual(response.status_code, 302)

    def test_cases_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cases"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/cases.html")
        self.assertContains(response, "<h1>Show all cases for Logged in User</h1>")
        self.assertContains(response, "Test Case created at")
