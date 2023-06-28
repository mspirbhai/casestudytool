from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from pages.models import Case, CaseLog, Project, TrackedMetric


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        # Test if the root URL returns a 200 status code
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # Test if a non-existent URL returns a 404 status code
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)

        # Test if a URL with an incorrect method returns a 405 status code
        response = self.client.post("/")
        self.assertEqual(response.status_code, 405)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")


class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
        )
        cls.url = reverse("projects")
        cls.tracked_metric_1 = TrackedMetric.objects.create(
            name="Test Metric",
            explanation="Descripton",
            calculation="SUM",
            units="Units",
        )
        cls.tracked_metric_2 = TrackedMetric.objects.create(
            name="Test Metric 2",
            explanation="Descripton",
            calculation="MEA",
            units="Units",
        )
        cls.project1 = Project.objects.create(name="Project 1", case_target=2)
        cls.project2 = Project.objects.create(name="Project 2")
        cls.project1.author.set([cls.user])
        cls.project1.tracked_metrics.set([cls.tracked_metric_1, cls.tracked_metric_2])
        cls.case = Case.objects.create(
            name="Test Case",
            description="Descripton",
            project=Project.objects.get(name="Project 1"),
        )
        cls.caselog = CaseLog.objects.create(
            case=Case.objects.get(name="Test Case"),
            tracked_value=10,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric"),
            author=cls.user,
        )
        cls.caselog = CaseLog.objects.create(
            case=Case.objects.get(name="Test Case"),
            tracked_value=10,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric 2"),
            author=cls.user,
        )
        cls.caselog = CaseLog.objects.create(
            case=Case.objects.get(name="Test Case"),
            tracked_value=20,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric 2"),
            author=cls.user,
        )

    def test_project_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/projects.html")
        self.assertContains(response, self.project1.name)
        self.assertContains(response, "Case status: 1 / 2")
        self.assertContains(response, "Metric name = Test Metric")
        self.assertContains(response, "Calculation = Sum")
        self.assertContains(response, "Value = 10Units")
        self.assertContains(response, "Metric name = Test Metric 2")
        self.assertContains(response, "Calculation = Mean")
        self.assertContains(response, "Value = 15Units")
        self.assertNotContains(response, self.project2.name)


class CasepageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
        )
        cls.tracked_metric_1 = TrackedMetric.objects.create(
            name="Test Metric",
            explanation="Descripton",
            calculation="SUM",
            units="Units",
        )
        cls.tracked_metric_2 = TrackedMetric.objects.create(
            name="Test Metric 2",
            explanation="Descripton",
            calculation="MEA",
            units="Units",
        )
        cls.project1 = Project.objects.create(name="Project 1", case_target=2)
        cls.project2 = Project.objects.create(name="Project 2")
        cls.project1.author.set([cls.user])
        cls.project1.tracked_metrics.set([cls.tracked_metric_1, cls.tracked_metric_2])
        cls.case = Case.objects.create(
            name="Test Case",
            description="Descripton",
            project=Project.objects.get(name="Project 1"),
        )
        cls.case_2 = Case.objects.create(
            name="Test Case 2",
            description="Descripton",
            project=Project.objects.get(name="Project 2"),
        )
        cls.caselog = CaseLog.objects.create(
            title="Test CaseLog 1",
            case=Case.objects.get(name="Test Case"),
            tracked_value=10,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric"),
            author=cls.user,
        )
        cls.caselog = CaseLog.objects.create(
            title="Test CaseLog 2",
            case=Case.objects.get(name="Test Case"),
            tracked_value=10,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric 2"),
            author=cls.user,
        )
        cls.caselog = CaseLog.objects.create(
            title="Test CaseLog 3",
            case=Case.objects.get(name="Test Case 2"),
            tracked_value=20,
            tracked_metric=TrackedMetric.objects.get(name="Test Metric 2"),
            author=cls.user,
        )

    def test_cases_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/cases/" + str(self.project1.pk) + "/")
        self.assertEqual(response.status_code, 302)

    def test_cases_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("cases", kwargs={"pk": self.project1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/cases.html")
        self.assertContains(response, "Show All Cases For Project: Project 1")
        self.assertContains(response, 'href="/projects/">Back')
        self.assertContains(
            response, 'href="/cases/' + str(self.project1.pk) + '/new/">New Case'
        )
        self.assertContains(response, "Test Case")
        self.assertNotContains(response, "Test Case 2")
        self.assertContains(response, 'href="/caselog/' + str(self.case.pk) + '/"')
        self.assertContains(response, "Test CaseLog 1")
        self.assertContains(response, "Test CaseLog 2")
        self.assertNotContains(response, "Test CaseLog 3")

    def test_case_creation(self):
        self.client.force_login(self.user)
        data = {
            "name": "Test Case 5",
            "description": "This is a test case.",
            "project": self.project1.pk,
        }
        response = self.client.post(
            reverse("cases_new", kwargs={"pk": self.project1.pk}), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("cases", kwargs={"pk": self.project1.pk})
        )
        self.assertEqual(Case.objects.last().name, "Test Case 5")
        self.assertEqual(Case.objects.last().description, "This is a test case.")


class CaseLogsPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="Mustafa", email="mustafa@dev.io", password="some_pass"
        )
        cls.project = Project.objects.create(name="Test Project")
        cls.case = Case.objects.create(
            name="Test Case",
            description="Descripton",
            project=Project.objects.get(name="Test Project"),
        )
        cls.caselog = CaseLog.objects.create(
            title="Test Case Log 1",
            case=cls.case,
            author=cls.user,
            body="Test Case Log 1 Body Text",
        )

    def test_caselog_list_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("caselogs", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/caselog.html")
        self.assertContains(response, "Show All Caselogs for Case: Test Case")
        self.assertContains(
            response, 'href="/cases/' + str(self.project.pk) + '/">Back'
        )
        self.assertContains(
            response, 'href="/caselog/new/' + str(self.case.pk) + '/">New Case'
        )
        self.assertContains(
            response, 'href="/caselog_detail/' + str(self.caselog.pk) + '/"'
        )
        self.assertContains(
            response,
            '<h3 class="display-6 link-body-emphasis mb-1">'
            + self.caselog.title
            + "</h3>",
        )

    def test_caselogs_url_exists_at_correct_location_and_redirects_to_login(self):
        caselog_url = "/caselog/" + str(self.caselog.pk) + "/"
        response = self.client.get(caselog_url)
        self.assertEqual(response.status_code, 302)

    def test_caselog_detail_caselog_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("caselog_detail", kwargs={"pk": self.caselog.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/caselog_detail.html")
        self.assertContains(response, 'href="/caselog/' + str(self.case.pk) + '/">Back')
        self.assertContains(
            response, 'href="/caselog/edit/' + str(self.caselog.pk) + '/">Edit'
        )
        self.assertContains(response, self.caselog.title)

    def test_caselog_create(self):
        self.client.force_login(self.user)
        data = {
            "title": "Test Case Log 2",
            "author": self.user,
            "case": self.case,
            "body": "This is a test case log.",
        }

        response = self.client.post(
            reverse("caselog_new", kwargs={"pk": self.case.pk}), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "caselog_detail",
                kwargs={"pk": CaseLog.objects.latest("updated_at").pk},
            ),
        )

        self.assertEqual(CaseLog.objects.latest("updated_at").author, self.user)
        self.assertEqual(CaseLog.objects.latest("updated_at").title, "Test Case Log 2")
        self.assertEqual(CaseLog.objects.latest("updated_at").case, self.case)
        self.assertEqual(
            CaseLog.objects.latest("updated_at").body,
            "This is a test case log.",
        )

    def test_caselog_edit(self):
        self.client.force_login(self.user)
        data = {
            "title": "Test Case Log 3",
            "body": "This is a test case log edited.",
        }
        response = self.client.post(
            reverse(
                "caselog_edit", kwargs={"pk": CaseLog.objects.latest("updated_at").pk}
            ),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "caselog_detail", kwargs={"pk": CaseLog.objects.latest("updated_at").pk}
            ),
        )
        self.assertEqual(CaseLog.objects.latest("updated_at").author, self.user)
        self.assertEqual(CaseLog.objects.latest("updated_at").title, "Test Case Log 3")
        self.assertEqual(CaseLog.objects.latest("updated_at").case, self.case)
        self.assertEqual(
            CaseLog.objects.latest("updated_at").body, "This is a test case log edited."
        )
