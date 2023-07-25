from django.test import TestCase
from django.urls import reverse


class GoogleLoginTestCase(TestCase):
    def test_google_login(self):
        response = self.client.get(reverse('social:begin', args=['google']))
        self.assertEqual(response.status_code, 302)
        self.assertIn('accounts.google.com', response.url)


class GitHubLoginTestCase(TestCase):
    def test_github_login(self):
        response = self.client.get(reverse('social:begin', args=['github']))
        self.assertEqual(response.status_code, 302)
        self.assertIn('github.com', response.url)
