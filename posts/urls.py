from django.urls import path
from .views import home, post_detail, post_publish, post_edit, \
    post_delete, user_signup, user_signin, user_signout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
