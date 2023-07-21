from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Person, Post


class ModelCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.person = Person.objects.create(user=self.user, bio='Test bio', photo='test.jpg')
        self.person2 = Person.objects.create(user=self.user2, bio='Test bio2', photo='test2.jpg')
        self.post = Post.objects.create(user=self.user, photo='test_photo.jpg', description='Test description')
        self.post2 = Post.objects.create(user=self.user2, photo='test_photo2.jpg', description='Test description2')

    def test_person_creation(self):
        self.assertEqual(self.person.user, self.user)
        self.assertEqual(self.person.bio, 'Test bio')
        self.assertEqual(self.person.photo, 'test.jpg')

    def test_post_creation(self):
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.photo, 'test_photo.jpg')
        self.assertEqual(self.post.description, 'Test description')

    def test_get_db(self):
        persons = Person.objects.all()
        posts = Post.objects.all()
        self.assertEqual(persons.count(), 2)
        self.assertEqual(posts.count(), 2)

    def test_delete_bd(self):
        person_objects = Person.objects.first()
        person_id = person_objects.id
        user_id = person_objects.user
        person_post = Post.objects.filter(user=person_objects.user).first()
        user_id.delete()
        self.assertFalse(Person.objects.filter(id=person_id).exists())
        self.assertFalse(Post.objects.filter(id=person_post.id).exists())
