import uuid

def test_register(client):
    unique_id = str(uuid.uuid4())[:8]

    data = {
        "username": f"user_{unique_id}",
        "email": f"{unique_id}@mail.com",
        "password": "123"
    }

    res = client.post('/register', json=data)
    assert res.status_code == 201

    # Duplicate user 
    res = client.post('/register', json=data)
    assert res.status_code == 400


def test_register_missing_fields(client):
    res = client.post('/register', json={})
    assert res.status_code == 400


def test_login(client):
    unique_id = str(uuid.uuid4())[:8]

    username = f"user_{unique_id}"

    client.post('/register', json={
        "username": username,
        "email": f"{unique_id}@mail.com",
        "password": "123"
    })

    res = client.post('/login', json={
        "username": username,
        "password": "123"
    })

    assert res.status_code == 200


def test_invalid_login(client):
    res = client.post('/login', json={
        "username": "wrong",
        "password": "wrong"
    })
    assert res.status_code == 401