from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_http_methods


def index(request):
    return HttpResponse("Hello from index")


@require_GET
def home(request):
    pass


@require_GET
def post_detail(request, post_id):
    pass


@require_http_methods(["GET", "POST"])
def post_create(request):
    pass


@require_http_methods(["GET", "POST"])
def post_update(request, post_id):
    pass


@require_GET
def post_delete(request):
    pass


@require_http_methods(["GET", "POST"])
def user_signup(request):
    pass


@require_http_methods(["GET", "POST"])
def user_signin(request):
    pass


@require_GET
def user_signout(request):
    pass
