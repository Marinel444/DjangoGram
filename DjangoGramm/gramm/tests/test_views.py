from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Person, Post
from PIL import Image
import io


def temporary_image():
    bts = io.BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class MyViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.person = Person.objects.create(user=self.user, bio='Test bio')
        self.post = Post.objects.create(user=self.user, photo='test_photo.jpg', description='Test description')

    def test_view_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gramm/index.html')

    def test_view_login(self):
        response = self.client.get(reverse('login'))
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gramm/login.html')

    def test_view_register(self):
        data = {
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(reverse('register'), data)
        user = User.objects.filter(username='testuser2').first()
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(user.username, 'testuser2')
        self.assertEqual(User.objects.count(), 2)

    def test_create_post(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('add_post'),
                                    {'photo': temporary_image(), 'description': 'New post',
                                     'user': self.user.id}, format='multipart')
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(Post.objects.count(), 2)
