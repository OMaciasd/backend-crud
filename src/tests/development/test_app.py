import pytest
from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index route."""
    response = client.get('/')
    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )
    if b'Welcome to the CRUD API' not in response.data:
        raise ValueError(
            "Response data does not contain 'Welcome to the CRUD API'"
        )


def test_get_items_empty(client):
    """Test GET /api/items on empty data."""
    response = client.get('/api/items')
    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )
    if response.get_json() != []:
        raise ValueError(
            f"Expected an empty items list, but got: {response.get_json()}"
        )


def test_add_item(client):
    """Test adding an item."""
    response = client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    if response.status_code != 201:
        raise ValueError(
            f"Expected status code 201, but got {response.status_code}"
        )
    if response.get_json() != {
        "name": "Item 1",
        "description": "Un item de prueba"
    }:
        raise ValueError(
            f"Expected item data to be {{'name': 'Item 1', "
            "'description': 'Un item de prueba'}}, "
            f"but got {response.get_json()}"
        )


def test_get_items_after_add(client):
    """Test GET /api/items after adding an item."""
    client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    response = client.get('/api/items')

    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )

    expected_response = [{
        "name": "Item 1",
        "description": "Un item de prueba"
    }]

    if response.get_json() != expected_response:
        raise ValueError(
            f"Expected items list to be {expected_response}, "
            f"but got {response.get_json()}"
        )


def test_update_item(client):
    """Test updating an item."""
    client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    response = client.put('/api/items/0', json={
        "name": "Updated Item",
        "description": "Updated description"
    })
    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )
    if response.get_json() != {
        "name": "Updated Item",
        "description": "Updated description"
    }:
        raise ValueError(
            f"Expected updated item data to be {{'name': 'Updated Item', "
            "'description': 'Updated description'}}, "
            f"but got {response.get_json()}"
        )


def test_get_items_after_update(client):
    """Test GET /api/items after updating an item."""
    client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    client.put('/api/items/0', json={
        "name": "Updated Item",
        "description": "Updated description"
    })
    response = client.get('/api/items')
    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )
    if response.get_json() != [{
        "name": "Updated Item",
        "description": "Updated description"
    }]:
        raise ValueError(
            "Expected items list to be [{'name': 'Updated Item', "
            "'description': 'Updated description'}], "
            f"but got {response.get_json()}"
        )


def test_delete_item(client):
    """Test deleting an item."""
    client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    response = client.delete('/api/items/0')
    if response.status_code != 204:
        raise ValueError(
            f"Expected status code 204, but got {response.status_code}"
        )


def test_get_items_after_delete(client):
    """Test GET /api/items after deleting an item."""
    client.post('/api/items', json={
        "name": "Item 1",
        "description": "Un item de prueba"
    })
    client.delete('/api/items/0')
    response = client.get('/api/items')
    if response.status_code != 200:
        raise ValueError(
            f"Expected status code 200, but got {response.status_code}"
        )
    if response.get_json() != []:
        raise ValueError(
            f"Expected items list to be [], but got {response.get_json()}"
        )


def test_update_nonexistent_item(client):
    """Test updating a non-existent item."""
    response = client.put('/api/items/999', json={"name": "Should Fail"})
    if response.status_code != 404:
        raise ValueError(
            f"Expected status code 404, but got {response.status_code}"
        )
    if response.get_json().get('error') != 'Item not found':
        raise ValueError(
            f"Expected error message 'Item not found', but got "
            f"{response.get_json().get('error')}"
        )


def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item."""
    response = client.delete('/api/items/999')
    if response.status_code != 404:
        raise ValueError(
            f"Expected status code 404, but got {response.status_code}"
        )
    if response.get_json().get('error') != 'Item not found':
        raise ValueError(
            f"Expected error message 'Item not found', but got "
            f"{response.get_json().get('error')}"
        )
