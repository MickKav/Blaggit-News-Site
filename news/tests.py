from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

class PostTests(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', 
            password = 'testpassword')
        self.post = Post.objects.create(
            title = 'Test Post',
            content = 'This is a test post content.',
            author = self.user,
        )


    def tearDown(self):
        # Clean up resources created during the test
        self.user.delete()
        self.post.delete()


    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', 
            kwargs = {'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)


    def test_post_add_view(self):
        self.client.login(username = 'testuser', password = 'testpassword')

        response = self.client.post(reverse('post_add'), 
            data = {'title': 'New Test Post', 'content': 'Test content'})
        self.assertEqual(response.status_code, 302)

        new_post = Post.objects.get(title = 'New Test Post')
        self.assertEqual(new_post.author, self.user)