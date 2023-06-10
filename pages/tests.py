from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from pages.models import Case, CaseLog


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
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
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
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
        )
        cls.case = Case.objects.create(case_name="Test Case", description="Descripton")

    def test_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/cases/")
        self.assertEqual(response.status_code, 302)

    def test_cases_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cases"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/cases.html")
        self.assertContains(response, "<h1>Show All Cases For Logged In User</h1>")
        self.assertContains(response, '<h5 class="mb-1">Test Case</h5>')


class CaseLogsPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
        )
        cls.case = Case.objects.create(case_name="Test Case", description="Descripton")
        cls.caselog = CaseLog.objects.create(
            title="Test Case Log 1",
            case_name=cls.case,
            author=cls.user,
            body="Test Case Log 1 Body Text",
        )

    def test_cases_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/cases/1/")
        self.assertEqual(response.status_code, 302)

    def test_caselog_list_with_pk_1_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("caselogs", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/caselogs.html")
        self.assertContains(response, "<h1>Show all case logs for Logged in User</h1>")
        self.assertContains(response, '<h5 class="mb-1">Test Case Log 1</h5>')

    def test_caselogs_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/caselogs/1/")
        self.assertEqual(response.status_code, 302)

    def test_caselog_detail_with_pk_1_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("caselog_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/caselog_detail.html")
        self.assertContains(
            response, "<h1>Show Details for Case log Test Case for Logged in User</h1>"
        )
        self.assertContains(
            response, "<h2>Test Case Log 1 written by mustafa@dev.io</h2>"
        )
