from .models import Comment, Post, Category
from django import forms


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'featured_image', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.choices = Category.objects.all().values_list(
            "name", "name"
        )

    class Meta:
        model = Post
        fields = ["title", "featured_image", "content", "category", "status"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"readonly": True}),
        }