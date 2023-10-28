from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


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


class PostDelete(View):

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'post_delete.html', {'post': post})


class AddPost(CreateView):
    model = Post
    template_name = 'post_add.html'
    fields = '__all__'


class PostEdit(View):

    def get(self, request, slug):
        return render(request, 'post_edit.html')

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))