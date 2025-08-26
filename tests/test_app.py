from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.fast_zero.app import app

client = TestClient(app)


def test_root_endpoint(client):
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to the Fast Zero API!'}


def test_create_user(client):
    client = TestClient(app)

    response = client.post(
        '/users',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testuser@example.com',
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testuser',
                'email': 'testuser@example.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'newsecret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}
