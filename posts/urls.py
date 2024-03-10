from django.urls import path
from .views import index, home, post_detail, post_publish, post_edit, \
    post_delete, user_signup, user_signin, user_signout

urlpatterns = [
    path("", index, name="index"),
    path("home/", home, name="home"),
    path("post/<int:post_pk>/", post_detail),
    path("post_publish/", post_publish),
    path("post/<int:post_pk>/edit/", post_edit),
    path("post/<int:post_pk>/delete/", post_delete),
]

users = [
    path("signup/", user_signup),
    path("signin/", user_signin),
    path("signout/", user_signout),
]

urlpatterns += users
