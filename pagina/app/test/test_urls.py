
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import index

class TestUrls(SimpleTestCase):
    def test_url_resuelve_a_vista(self):
        url = reverse('inicio')
        self.assertEqual(resolve(url).func, index)
