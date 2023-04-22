from django.urls import path
from .views import post_create_view,post_list_view,post_update_view,post_delete_view,PostLikeView,post_detail_view

app_name = "posts"

urlpatterns = [
    path("",post_list_view,name="list"),
    path("add/",post_create_view,name="add"),
    path("<int:pk>/",post_detail_view,name="detail"),
    path("<int:pk>/edit/",post_update_view,name="edit"),
    path("<int:pk>/delete/",post_delete_view,name="delete"),
    path("<int:pk>/post_like/",PostLikeView,name="like"),
]