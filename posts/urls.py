from django.urls import path
from .views import index, home, post_detail, post_publish, post_edit, post_delete


urlpatterns = [
    path("", index, name="index"),
    path("home/", home, name="home"),
    path("post/<int:post_pk>/", post_detail),
    path("post_publish/", post_publish),
    path("post/<int:post_pk>/edit/", post_edit),
    path("post/<int:post_pk>/delete/", post_delete),
]
