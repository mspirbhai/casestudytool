from django.test import TestCase
from django.test import SimpleTestCase

# Create your tests here.


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location_and_redirects_to_login(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 302)
