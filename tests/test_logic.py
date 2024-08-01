import pytest
from http import HTTPStatus

from .api_endpoints import GET_TASKS_URL, SET_ACCESS_URL


@pytest.mark.django_db
def test_task_access_creation(
    authenticated_user_client, authenticated_author_client,
    task, access_data
):
    response = authenticated_user_client.get(f'{GET_TASKS_URL}{task.id}/')
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = authenticated_author_client.post(
        SET_ACCESS_URL, data=access_data
    )
    assert response.status_code == HTTPStatus.CREATED
    response = authenticated_user_client.get(f'{GET_TASKS_URL}{task.id}/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_task_visibility(
    authenticated_author_client, authenticated_user_client,
    author, task
):
    # Получаем начальное количество заметок у пользователя и автора
    response = authenticated_user_client.get(GET_TASKS_URL)
    user_tasks_before = len(response.json())
    response = authenticated_author_client.get(GET_TASKS_URL)
    author_tasks_before = len(response.json())

    new_task_data = {
        'title': 'test title',
        'description': 'test description'
    }
    response = authenticated_author_client.post(
        GET_TASKS_URL, data=new_task_data
    )
    assert response.status_code == HTTPStatus.CREATED

    response = authenticated_user_client.get(GET_TASKS_URL)
    assert len(response.json()) == user_tasks_before

    response = authenticated_author_client.get(GET_TASKS_URL)
    assert len(response.json()) == author_tasks_before + 1
