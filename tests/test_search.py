import uuid

def test_search(client):
    unique_id = str(uuid.uuid4())[:8]

    username = f"search_{unique_id}"

    client.post('/students', json={
        "username": username,
        "email": f"{unique_id}@mail.com",
        "password": "123"
    })

    res = client.get(f'/search?q=search_')
    assert res.status_code == 200

    data = res.get_json()["data"]
    assert any(username in u["username"] for u in data)