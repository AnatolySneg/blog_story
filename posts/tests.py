from django.test import TestCase
# TODO: Add some view tests

from django.test import TestCase, Client
import unittest
from .models import Post
from django.contrib.auth.models import User

client = Client()

user_1 = {"id": 1, 'username': "username_1", "email": "example_1@example.com", 'password': "qwerty"}
user_2 = {"id": 2, 'username': "username_2", "email": "example_2@example.com", 'password': "qwerty"}
user_3 = {"id": 3, 'username': "username_3", "email": "example_3@example.com", 'password': "qwerty"}

post_1 = {"id": 1, "user_id": 1, "title": "Title_1", "text": "Text_1_Text_text"}
post_2 = {"id": 2, "user_id": 2, "title": "Title_2", "text": "Text_2_Text_text"}
post_3 = {"id": 3, "user_id": 3, "title": "Title_3", "text": "Text_3_Text_text"}
post_4 = {"id": 4, "user_id": 1, "title": "Title_4", "text": "Text_4_Text_text"}
post_5 = {"id": 5, "user_id": 1, "title": "Title_5", "text": "Text_5_Text_text"}
post_6 = {"id": 6, "user_id": 1, "title": "Title_6", "text": "Text_6_Text_text"}


