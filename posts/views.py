from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from .forms import PostCommentForm
from .models import Post, PostComment


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'contents', 'category']
    success_url = reverse_lazy("posts:list")
    success_message = "Post został dodany!"

    def form_valid(self, form: BaseForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


post_create_view = PostCreateView.as_view()


class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = "posts/post_list.html"
    context_object_name = "object_list"

    def get_queryset(self) -> QuerySet:
        return Post.objects.select_related('user', 'category').prefetch_related('likes').order_by("-created_datetime")


post_list_view = PostListView.as_view()


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'contents', 'category']
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("posts:list")
    success_message = "Post został zaktualizowany!"


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:list")
    success_message = "Post został usunięty!"
    template_name = "posts/post_confirm_delete.html"


post_delete_view = PostDeleteView.as_view()


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"


post_detail_view = PostDetailView.as_view()


@login_required
def PostLikeView(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=pk)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect("posts:list")


@login_required
def add_comment_view(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("posts:detail", pk=pk)
    else:
        form = PostCommentForm()

    return render(request, "posts/postcomment_form.html", context={'form': form, 'post': post})
