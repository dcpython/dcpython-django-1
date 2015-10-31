from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


class DCPythonTest(TestCase):
    def setUp(self):
        self.c = Client()

    def assert200(self, name):
        response = self.c.get(reverse(name), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_about(self):
        self.assert200('about')

    def test_get_contact(self):
        self.assert200('contact')

    def test_get_deals(self):
        self.assert200('deals')

    def test_get_home(self):
        self.assert200('home')

    def test_get_legal(self):
        self.assert200('legal')

    def test_get_make_donation(self):
        self.assert200('make_donation')

    def test_get_resources(self):
        self.assert200('resources')

    def test_get_support(self):
        self.assert200('support')
