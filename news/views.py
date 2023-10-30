from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Category
from .forms import CommentForm, PostForm, PostEditForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        disliked = False
        if post.up_vote.filter(id=self.request.user.id).exists():
            liked = True
        elif post.down_vote.filter(id=self.request.user.id).exists():
            disliked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "disliked": disliked,
                "comment_form": CommentForm(),
            },
        )
        
    
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        disliked = False
        if post.up_vote.filter(id=self.request.user.id).exists():
            liked = True
        elif post.down_vote.filter(id=self.request.user.id).exists():
            disliked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()
        
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "disliked": disliked,
                "comment_form": CommentForm(),
            },
        )


class PostVote(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        vote_direction = request.POST.get('vote')

        if vote_direction == 'up':
            if post.up_vote.filter(id=request.user.id).exists():
                post.up_vote.remove(request.user)
            else:
                if post.down_vote.filter(id=request.user.id).exists():
                    post.down_vote.remove(request.user)

                post.up_vote.add(request.user)

        if vote_direction == 'down':
            if post.down_vote.filter(id=request.user.id).exists():
                post.down_vote.remove(request.user)
            else:
                if post.up_vote.filter(id=request.user.id).exists():
                    post.up_vote.remove(request.user)

                post.down_vote.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'post_delete.html', {'post': post})


@method_decorator(login_required, name = 'dispatch')
class AddPost(CreateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        return response

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})


class PostEdit(View):
    template_name = 'post_edit.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostEditForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        return render(request, self.template_name, {'form': form, 'post': post})

class AddCategory(CreateView):
    model = Category
    template_name = 'post_category.html'
    fields = '__all__'


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    categories = Category.objects.all()
    return render(request, 'categories.html', {'cats':cats, 'category_posts':category_posts, 'categories': categories})