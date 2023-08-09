import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Person, Post, Follower
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

    def test_like(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.post(reverse('like'), {'post_id': self.post.pk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertEqual(data['like_count'], 1)

        response = client.post(reverse('like'), {'post_id': self.post.pk})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['like_count'], 0)


class AccountUserViewFollowerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')
        self.profile1 = Person.objects.create(user=self.user1, bio='Test bio 1')
        self.profile2 = Person.objects.create(user=self.user2, bio='Test bio 2')
        self.post1 = Post.objects.create(user=self.user2, photo='test.jpg', description='Test post 1')
        self.post2 = Post.objects.create(user=self.user1, photo='test.jpg', description='Test post 2')

    def test_account_user_view(self):
        client = Client()
        client.login(username='user1', password='testpassword1')
        response = client.get(reverse('account', args=[self.user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.profile2)
        self.assertEqual(list(response.context['posts']), [self.post1])

        client.logout()
        response = client.get(reverse('account', args=[self.user1.id]))
        self.assertEqual(response.status_code, 302)

        client.login(username='user2', password='testpassword2')
        response = client.get(reverse('account', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.profile1)
        self.assertEqual(list(response.context['posts']), [self.post2])

    def test_subscribe(self):
        client = Client()
        client.login(username='user2', password='testpassword2')
        self.assertFalse(Follower.objects.filter(follower_id=self.user1, following_user_id=self.user2).exists())

        response = client.post(reverse('account', args=[self.user1.id]), {'action': 'subscribe'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Follower.objects.filter(follower_id=self.user1, following_user_id=self.user2).exists())

        response = client.post(reverse('account', args=[self.user1.id]), {'action': 'unsubscribe'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Follower.objects.filter(follower_id=self.user1, following_user_id=self.user2).exists())
