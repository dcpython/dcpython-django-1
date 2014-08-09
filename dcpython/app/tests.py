from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


class DCPythonTest(TestCase):

    def test_get_requests(self):
        """
        Tests that the url routes return a 200 status code.
        """
        c = Client()
        routes = map(reverse, ['about', 'contact', 'deals', 'home', 'legal', 'make_donation', 'resources', 'donate'])
        for route in routes:
            response = c.get(route)
            self.assertEqual(response.status_code, 200)
