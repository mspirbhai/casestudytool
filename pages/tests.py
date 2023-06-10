from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "pages/home.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<title>Home page</title>")


class AboutpageTests(TestCase):
    def test_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name_and_redirects_to_login(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):
        User = get_user_model()
        user = User.objects.create_user("Mustafa," "mustafa@dev.io", "some_pass")
        self.client.force_login(user)
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "pages/about.html")

    def test_template_content(self):
        User = get_user_model()
        user = User.objects.create_user("Mustafa," "mustafa@dev.io", "some_pass")
        self.client.force_login(user=user)
        response = self.client.get(reverse("about"))
        self.assertContains(response, "<h1>About page</h1>")
