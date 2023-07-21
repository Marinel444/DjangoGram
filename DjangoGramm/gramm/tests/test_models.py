from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Person, Post, Like, Follower


class ModelCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.person = Person.objects.create(user=self.user, bio='Test bio', photo='test.jpg')
        self.person2 = Person.objects.create(user=self.user2, bio='Test bio2', photo='test2.jpg')
        self.post = Post.objects.create(user=self.user, photo='test_photo.jpg', description='Test description')
        self.post2 = Post.objects.create(user=self.user2, photo='test_photo2.jpg', description='Test description2')
        self.like = Like.objects.create(person_id=self.user, post=self.post)
        self.like2 = Like.objects.create(person_id=self.user2, post=self.post2)
        self.follower = Follower.objects.create(follower_id=self.user, following_user_id=self.user2)

    def test_person_creation(self):
        self.assertEqual(self.person.user, self.user)
        self.assertEqual(self.person.bio, 'Test bio')
        self.assertEqual(self.person.photo, 'test.jpg')

    def test_post_creation(self):
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.photo, 'test_photo.jpg')
        self.assertEqual(self.post.description, 'Test description')

    def test_like_creation(self):
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.person_id, self.user)

    def test_follower_creation(self):
        self.assertEqual(self.follower.follower_id, self.user)
        self.assertEqual(self.follower.following_user_id, self.user2)

    def test_get_db(self):
        persons = Person.objects.all()
        posts = Post.objects.all()
        likes = Like.objects.all()
        follower = Follower.objects.all()
        self.assertEqual(follower.count(), 1)
        self.assertEqual(likes.count(), 2)
        self.assertEqual(persons.count(), 2)
        self.assertEqual(posts.count(), 2)

    def test_delete_bd(self):
        like_first = Like.objects.first()
        like_first.delete()

        follower = Follower.objects.first()
        follower.delete()

        like_objects = Like.objects.all()
        person_objects = Person.objects.first()
        person_id = person_objects.id
        user_id = person_objects.user
        person_post = Post.objects.filter(user=person_objects.user).first()
        user_id.delete()

        self.assertEqual(like_objects.count(), 1)
        self.assertFalse(Follower.objects.first())
        self.assertFalse(Person.objects.filter(id=person_id).exists())
        self.assertFalse(Post.objects.filter(id=person_post.id).exists())
