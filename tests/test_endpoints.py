from http import HTTPStatus

import pytest

from .api_endpoints import (
    CREATE_USER_URL, GET_TASKS_URL, GET_TOKEN_URL,
    SET_ACCESS_URL
)


@pytest.mark.django_db
def test_registration_and_login(api_client, user_data):
    response = api_client.post(CREATE_USER_URL, user_data)
    assert response.status_code == HTTPStatus.CREATED

    response = api_client.post(GET_TOKEN_URL, user_data)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint, expected_status',
    (
        (GET_TASKS_URL, HTTPStatus.UNAUTHORIZED),
        (lambda id: f'{GET_TASKS_URL}{id}/', HTTPStatus.UNAUTHORIZED),
        (SET_ACCESS_URL, HTTPStatus.UNAUTHORIZED),
    )
)
def test_pages_available_for_anonymous_user(
    api_client, endpoint, expected_status, task
):
    if callable(endpoint):
        endpoint = endpoint(task.id)
    response = api_client.get(endpoint)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint, expected_status',
    (
        (GET_TASKS_URL, HTTPStatus.OK),
        (lambda id: f'{GET_TASKS_URL}{id}/', HTTPStatus.OK),
    )
)
def test_authenticated_user(
    authenticated_author_client, task, endpoint, expected_status
):
    if callable(endpoint):
        endpoint = endpoint(task.id)

    response = authenticated_author_client.get(endpoint)
    assert response.status_code == expected_status
