from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User


class PostTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
        )

    def tearDown(self):
        # Clean up resources created during the test
        if hasattr(self, 'user'):
            self.user.delete()
        if hasattr(self, 'post'):
            self.post.delete()

    def test_post_detail_view(self):
        response = self.client.get(reverse('news:post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_post_add_view(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('news:post_add'), 
                                    data={'title': 'New Test Post', 'content': 'Test content'})
        self.assertEqual(response.status_code, 302)

        new_post = Post.objects.get(title='New Test Post')
        self.assertEqual(new_post.author, self.user)

    def test_category_add_view(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('news:add_category'), {'name': 'Test Category'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200) 