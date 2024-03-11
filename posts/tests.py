from django.test import TestCase, Client
from .models import Post
from django.contrib.auth.models import User

client = Client()

user_1 = {"id": 1, 'username': "username_1", "email": "example_1@example.com", 'password': "qwerty"}
user_2 = {"id": 2, 'username': "username_2", "email": "example_2@example.com", 'password': "qwerty"}
user_3 = {"id": 3, 'username': "username_3", "email": "example_3@example.com", 'password': "qwerty"}

post_1 = {"id": 1, "author_id": 1, "title": "Title_1", "text": "Text_1_Text_text"}
post_2 = {"id": 2, "author_id": 2, "title": "Title_2", "text": "Text_2_Text_text"}
post_3 = {"id": 3, "author_id": 3, "title": "Title_3", "text": "Text_3_Text_text"}
post_4 = {"id": 4, "author_id": 1, "title": "Title_4", "text": "Text_4_Text_text"}
post_5 = {"id": 5, "author_id": 1, "title": "Title_5", "text": "Text_5_Text_text"}
post_6 = {"id": 6, "author_id": 1, "title": "Title_6", "text": "Text_6_Text_text"}


class ViewsTesting(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(**user_1)
        User.objects.create_user(**user_2)
        User.objects.create_user(**user_3)

        Post.objects.create(**post_1)
        Post.objects.create(**post_2)
        Post.objects.create(**post_3)
        Post.objects.create(**post_4)
        Post.objects.create(**post_5)
        Post.objects.create(**post_6)

    def test_get_posts(self):
        response = client.get("/home/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        response = client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Title_1")
        self.assertContains(response, "Text_1_Text_text")

    def test_post_detail_not_exist(self):
        response = client.get("/post/112/")
        self.assertEqual(response.status_code, 404)

    def test_post_publish_unauthorized(self):
        response = client.post("/post_publish/", {'title': 'New Post', 'text': 'This is a new post.'})
        self.assertEqual(response.status_code, 401)

    def test_post_edit_unauthorized(self):
        response = client.post("/post/1/edit/", {'title': 'Updated Post', 'text': 'This is an updated post.'})
        self.assertEqual(response.status_code, 401)

    def test_post_delete_unauthorized(self):
        response = client.get("/post/1/delete/")
        self.assertEqual(response.status_code, 401)


class ViewsTestingAuthorized(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(**user_1)
        self.client.force_login(self.user)

    def test_post_publish(self):
        response = self.client.post("/post_publish/", {'title': 'New Post', 'text': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())


class ViewsTestingErrorHandling(TestCase):
    def test_post_detail_404(self):
        response = client.get("/post/999/")
        self.assertEqual(response.status_code, 404)
