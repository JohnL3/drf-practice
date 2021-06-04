from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post
# pylint: disable=no-member


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='a', password='pass')

    def test_can_list_posts(self):
        a = User.objects.get(username='a')
        Post.objects.create(owner=a, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, len(response.data))

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        print(response.data, len(response.data))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        a = User.objects.create_user(username='a', password='pass')
        b = User.objects.create_user(username='b', password='pass')
        Post.objects.create(owner=a, title='a title', content='a content')
        Post.objects.create(owner=b, title='b title', content='b content')

    def test_can_retrieve_post_using_a_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_an_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_update_somebodys_elses_post(self):
        self.client.login(username='a', password='pass')
        response = self.client.put('/posts/2/', {'title': 'yay'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
