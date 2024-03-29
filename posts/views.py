from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_GET, require_http_methods
from .models import Post
from django.core import serializers
from .forms import UserSignupForm, PostForm
from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@require_GET
def home(request):
    posts = Post.objects.all().order_by("-edit_date")

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    data = serializers.serialize("json", posts)

    return HttpResponse(data, content_type="application/json")


@require_GET
def post_detail(request, post_pk):
    try:
        post = get_object_or_404(Post, pk=post_pk)
        serialized_post = {
            'author': post.author.username if post.author else None,
            'title': post.title,
            'text': post.text,
            'created_date': post.created_date,
            'edit_date': post.edit_date,
            # Serialize the image URL if available
            'title_image': post.title_image.url if post.title_image else None,
        }
        return JsonResponse({"post": serialized_post})
    except Http404:
        return JsonResponse({"error": f"Post with id={post_pk} does`t exist"}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def post_publish(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.edit_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect(post_detail, post_pk=post.pk)
        else:
            errors = dict(form.errors.items())
            return JsonResponse({"errors": errors}, status=400)
    post_fields = {"title": "", "text": "", "title_image": ""}
    return JsonResponse({"post_fields": post_fields})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def post_edit(request, post_pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    try:
        post = get_object_or_404(Post, pk=post_pk)
        if request.user.id != post.author.id:
            return JsonResponse({"error": "Another user is author of this post"}, status=403)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.edit_date = post.edit()
                post.save()
                return redirect(post_detail, post_pk=post.pk)
            else:
                errors = dict(form.errors.items())
                return JsonResponse({"errors": errors}, status=400)
        post_fields = {"title": post.title, "text": post.text, "title_image": post.title_image}
        return JsonResponse({"post_fields": post_fields})
    except Http404:
        return JsonResponse({"error": f"Post with id={post_pk} does`t exist"}, status=404)


@require_GET
def post_delete(request, post_pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    try:
        post = get_object_or_404(Post, pk=post_pk)
        if request.user != post.author:
            return JsonResponse({"error": "Another user is author of this post"}, status=403)
        post.delete()
        return redirect(home)
    except Http404:
        return JsonResponse({"error": f"Post with id={post_pk} does`t exist"}, status=404)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_signup(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse({"error": f"User {request.user.username} already authorised"}, status=400)
        user_form = UserSignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_user = authenticate(username=user.username, password=request.POST.get('password1'))
            django_login(request, auth_user)
            return JsonResponse({"status": f"User {user.username}, has been registered"}, status=201)
        else:
            errors = dict(user_form.errors.items())
            return JsonResponse({"errors": errors}, status=400)

    user_signup_fields = {"username": '', "email": '', "password1": '', "password2": ''}
    return JsonResponse({"user_signup_fields": user_signup_fields})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_signin(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return JsonResponse({"error": f"User {request.user.username} already authorized"}, status=400)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or username == '':
            return JsonResponse({"error": "Username required"}, status=400)
        if password is None or password == '':
            return JsonResponse({"error": "Password required"}, status=400)
        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            django_login(request, auth_user)
            return JsonResponse({"status": f"User {auth_user.username}, has been authorized"}, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

    user_signup_fields = {"username": '', "password": ''}
    return JsonResponse({"user_signup_fields": user_signup_fields})


@require_GET
def user_signout(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": f"User is unauthorised"}, status=400)
    username = request.user.username
    django_logout(request)
    return JsonResponse({"status": f"User {username}, has been unauthorised"}, status=200)
