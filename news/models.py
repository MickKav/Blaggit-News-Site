from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

STATUS = ((0, "Draft"), (1, "Published"))

class Category(models.Model):
    name = models.CharField(max_length = 200)
    approved = models.BooleanField(default = False)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length = 200, unique = True)
    slug = models.SlugField(max_length = 200, unique = True, blank = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, 
        related_name = "news_posts")
    updated_on = models.DateTimeField(auto_now = True)
    content = models.TextField(max_length = 240)
    featured_image = CloudinaryField('image', default = 'placeholder')
    excerpt = models.TextField(blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(choices = STATUS, default = 1)
    up_vote = models.ManyToManyField(User, 
        related_name = 'news_up_vote', blank = True)
    down_vote = models.ManyToManyField(User, 
        related_name = 'news_down_vote', blank = True)
    category = models.CharField(max_length = 200, default = 'news')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    def clean(self):
        super().clean()
        if len(self.title) < 5:
            raise ValidationError('Title must be at least 5 characters long.')


    def get_absolute_url(self):
        return reverse('post_detail', kwargs = {'slug': self.slug})

    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return self.title


    def number_of_up_votes(self):
        return self.up_vote.count()


    def number_of_down_votes(self):
        return self.down_vote.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, 
        on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    approved = models.BooleanField(default = False)

    class Meta:
        ordering = ['created_on']


    def __str__(self):
        return f"Comment {self.body} by {self.name}"