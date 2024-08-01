import pytest
from rest_framework.test import APIClient

from tasks.models import Task, User

from .api_endpoints import GET_TOKEN_URL


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def author():
    return User.objects.create_user(username='author', password='password')


@pytest.fixture
def task(author):
    return Task.objects.create(
        title='task 1', description='description 1', author=author
    )


@pytest.fixture
def user_token(api_client, user):
    response = api_client.post(
        GET_TOKEN_URL,
        {'username': user.username, 'password': 'password'}
    )
    return response.data['access']


@pytest.fixture
def author_token(api_client, author):
    response = api_client.post(
        GET_TOKEN_URL,
        {'username': author.username, 'password': 'password'}
    )
    return response.data['access']


@pytest.fixture
def authenticated_user_client(user_token):
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    return api_client


@pytest.fixture
def authenticated_author_client(author_token):
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + author_token)
    return api_client


@pytest.fixture
def user_data():
    return {'username': 'new_test_user', 'password': 'pass12371'}


@pytest.fixture
def access_data(user, task):
    return {'user': user.id, 'task': task.id, 'access': 'read'}
