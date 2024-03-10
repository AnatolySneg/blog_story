from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_GET, require_http_methods
from .models import Post
from django.core import serializers
from django.forms.models import model_to_dict
from .forms import UserSignupForm, UserSigninForm, PostForm
from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return JsonResponse({"message": "Hello from index"})


@require_GET
def home(request):
    posts = Post.objects.filter(published_date__isnull=False)
    data = serializers.serialize("json", posts)
    return HttpResponse(data, content_type="application/json")


# @csrf_exempt
@require_GET
def post_detail(request, post_pk):
    try:
        post = get_object_or_404(Post, pk=post_pk, published_date__isnull=False)
        return JsonResponse({"post": model_to_dict(post)})
    except Http404:
        return JsonResponse({"error": f"Post with id={post_pk} does`t exist"}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def post_publish(request):
    # TODO: add author validation
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post_pk=post.pk)
    post_fields = {"title": "", "text": "", }
    return JsonResponse({"post_fields": post_fields})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def post_edit(request, post_pk):
    # TODO: add author validation
    post = get_object_or_404(Post, pk=post_pk, published_date__isnull=False)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post_pk=post.pk)
    post_fields = {"title": post.title, "text": post.text}
    return JsonResponse({"post_fields": post_fields})


@require_GET
def post_delete(request, post_pk):
    # TODO: add author validation
    get_object_or_404(Post, pk=post_pk).delete()
    return redirect(home)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_signup(request):
    if request.method == "POST":
        user_form = UserSignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_user = authenticate(username=user.username, password=request.POST.get('password1'))
            if auth_user:
                django_login(request, auth_user)
            return redirect(home)
    user_signup_fields = {"username": '', "email": '', "password1": '', "password2": ''}
    return JsonResponse({"user_signup_fields": user_signup_fields})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_signin(request):
    if request.method == "POST":
        signin_form = UserSigninForm(request.POST)
        if signin_form.is_valid():
            user = signin_form.save()
            auth_user = authenticate(username=user.username, password=user.password)
            if auth_user:
                django_login(request, auth_user)
            return redirect(home)

    user_signup_fields = {"username": '', "password": ''}
    return JsonResponse({"user_signup_fields": user_signup_fields})


# TODO: Add require_authentication decorator!!!
@require_GET
def user_signout(request):
    django_logout(request)
    return redirect(home)
