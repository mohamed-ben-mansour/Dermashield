from django.test import TestCase

class SimpleSmokeTest(TestCase):
    def test_root_url(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])