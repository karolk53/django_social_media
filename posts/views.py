from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.forms import BaseForm, DateTimeInput
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostCommentForm

from .models import Post,PostComment
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView


# Create your views here.

class PostCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Post
    fields = ['title','contents','category']
    success_url = reverse_lazy("posts:list")
    success_message = "Added!"

    def form_valid(self, form: BaseForm) -> HttpResponse:
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


post_create_view = PostCreateView.as_view()


class PostListView(ListView):
    model = Post
    paginate_by = 3
    def get_queryset(self) -> QuerySet:
        return self.model.objects.order_by("-created_datetime")

post_list_view = PostListView.as_view()


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title','contents','category']
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("posts:list")


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy("posts:list")


post_delete_view = PostDeleteView.as_view()


@login_required
def PostLikeView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('posts:list'))


class PostDetailView(DetailView):
    model = Post


post_detail_view = PostDetailView.as_view()


@login_required
def add_comment_view(request,pk):
    if request.method == "POST" and request.user.is_authenticated:
        form = PostCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = Post.objects.get(pk=pk)
            instance.save()
    else:
        form = PostCommentForm()
    return render(request,"posts/postcomment_form.html",context={'form':form})
