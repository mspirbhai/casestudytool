from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from pages.models import Case, CaseLog
from pages.forms import CaseLogCreateForm
from pages.views import CaseLogCreateView


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")
        self.assertContains(response, "Home page")


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
        self.assertTemplateUsed(response, "pages/caselog.html")
        self.assertContains(response, "<h1>Show all case logs for Logged in User</h1>")
        self.assertContains(response, '<h5 class="mb-1">Test Case Log 1</h5>')

    def test_caselogs_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/caselog/1/")
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

    def test_case_creation(self):
        self.client.force_login(self.user)
        data = {
            "case_name": "Test Case 2",
            "description": "This is a test case.",
        }
        response = self.client.post(reverse("cases_new"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cases"))
        self.assertEqual(Case.objects.last().case_name, "Test Case 2")
        self.assertEqual(Case.objects.last().description, "This is a test case.")

    def test_caselog_create(self):
        self.client.force_login(self.user)
        data = {
            "title": "Test Case Log 2",
            "author": self.user,
            "case_name": self.case.case_name,
            "body": "This is a test case log.",
        }
        response = self.client.post(
            reverse("caselog_new", kwargs={"pk": self.case.pk}), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("caselog_detail", kwargs={"pk": CaseLog.objects.last().pk}),
        )
        self.assertEqual(CaseLog.objects.last().author, self.user)
        self.assertEqual(CaseLog.objects.last().title, "Test Case Log 2")
        self.assertEqual(CaseLog.objects.last().case_name, self.case)
        self.assertEqual(CaseLog.objects.last().body, "This is a test case log.")

    def test_caselog_edit(self):
        self.client.force_login(self.user)
        data = {
            "title": "Test Case Log 3",
            "body": "This is a test case log edited.",
        }
        response = self.client.post(
            reverse("caselog_edit", kwargs={"pk": CaseLog.objects.last().pk}), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("caselog_detail", kwargs={"pk": CaseLog.objects.last().pk}),
        )
        self.assertEqual(CaseLog.objects.last().author, self.user)
        self.assertEqual(CaseLog.objects.last().title, "Test Case Log 3")
        self.assertEqual(CaseLog.objects.last().case_name, self.case)
        self.assertEqual(CaseLog.objects.last().body, "This is a test case log edited.")
