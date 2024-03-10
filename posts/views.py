from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from .models import Post
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from .forms import UserSignupForm, UserLoginForm, PostForm
from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return JsonResponse({"message": "Hello from index"})
    # return HttpResponse("Hello from index")


@require_GET
def home(request):
    posts = Post.objects.filter(published_date__isnull=False)
    data = serializers.serialize("json", posts)
    return HttpResponse(data, content_type="application/json")


@require_GET
def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk, published_date__isnull=False)
    return JsonResponse({"post": model_to_dict(post)})


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
    else:
        post_fields = {"title": "", "text": "", }
    return JsonResponse({"post_fields": post_fields})


@require_http_methods(["GET", "POST"])
def post_edit(request, post_pk):
    # TODO: add author validation
    post = get_object_or_404(Post, pk=post_pk, published_date__isnull=False)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post_pk=post.pk)
    else:
        post_fields = {"title": post.title, "text": post.text}
    return JsonResponse({"post_fields": post_fields})


@require_http_methods(["DELETE"])
def post_delete(request, post_pk):
    # TODO: add author validation
    get_object_or_404(Post, pk=post_pk).delete()
    return redirect(home)


@require_http_methods(["GET", "POST"])
def user_signup(request):
    pass


@require_http_methods(["GET", "POST"])
def user_signin(request):
    pass


@require_GET
def user_signout(request):
    pass
