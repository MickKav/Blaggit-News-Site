from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post, Category
from .forms import CommentForm, PostForm, PostEditForm


@method_decorator(login_required, name='dispatch')
class AddPost(CreateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        response = super().form_valid(form)
        messages.success(self.request, 'Post created successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating post. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('news:post_detail', kwargs={'slug': self.object.slug})


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_slugs'] = [post.slug for post in context['post_list']]
        return context


class PostDetail(LoginRequiredMixin, View):
    login_url = 'account_login'

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
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        disliked = False

        if post.up_vote.filter(id=request.user.id).exists():
            liked = True
        elif post.down_vote.filter(id=request.user.id).exists():
            disliked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username

            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(request, "Your comment has been posted successfully.")

            return HttpResponseRedirect(reverse('news:post_detail', args=[slug]))

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "disliked": disliked,
                "comment_form": comment_form,
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

        return HttpResponseRedirect(reverse('news:post_detail', args=[slug]))


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news:home')

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        try:
            post.delete()
            messages.success(request, 'Post deleted successfully.')
            return HttpResponseRedirect(reverse('news:home'))
        except Exception as e:
            messages.error(request, f'Error deleting post: {e}')
        return HttpResponseRedirect(reverse('news:post_detail', args=[slug]))


@method_decorator(login_required, name = 'dispatch')
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
            messages.success(request, 'Post updated successfully.')
            return HttpResponseRedirect(reverse('news:post_detail', args=[slug]))
        else:
            messages.error(request, 'Error updating post. Please check the form.')
        return render(request, self.template_name, {'form': form, 'post': post})


@method_decorator(login_required, name='dispatch')
class AddCategory(CreateView):
    model = Category
    template_name = 'post_category.html'
    fields = '__all__'
    success_url = reverse_lazy('news:home')


def CategoryView(self, request, cats):
    category_posts = Post.objects.filter(category=cats)
    categories = Category.objects.all()
    return render(request, 'categories.html', {'cats': cats, 'category_posts': category_posts, 'categories': categories})