from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post, Comment
from .forms import CommentForm


def goodbye_view(request):
    return render(request, 'goodbye.html')



class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_date')

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment_text')
        if post_id and comment_text:
            try:
                post = Post.objects.get(id=post_id)
                Comment.objects.create(post=post, user=request.user, body=comment_text)
            except Post.DoesNotExist:
                pass
        return redirect('home')



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = post.comments.all().order_by('-created_date')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            return redirect('post_detail', slug=self.object.slug)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
