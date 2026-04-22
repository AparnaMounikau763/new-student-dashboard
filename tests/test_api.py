import uuid

def test_crud(client):
    unique_id = str(uuid.uuid4())[:8]

    username = f"api_{unique_id}"
    email = f"{unique_id}@mail.com"

    # POST
    res = client.post('/students', json={
        "username": username,
        "email": email,
        "password": "123"
    })
    assert res.status_code == 201

    # Duplicate POST 
    res = client.post('/students', json={
        "username": username,
        "email": email,
        "password": "123"
    })
    assert res.status_code == 400

    # GET
    res = client.get('/students')
    assert res.status_code == 200

    students = res.get_json()["data"]
    student_id = students[-1]["id"]

    # PUT
    res = client.put(f'/students/{student_id}', json={
        "username": f"updated_{unique_id}"
    })
    assert res.status_code == 200

    # PUT duplicate 
    client.post('/students', json={
        "username": "dup_user",
        "email": "dup@mail.com",
        "password": "123"
    })

    res = client.put(f'/students/{student_id}', json={
        "username": "dup_user"
    })
    assert res.status_code == 400

    # DELETE
    res = client.delete(f'/students/{student_id}')
    assert res.status_code == 200

    # DELETE non-existing 
    res = client.delete('/students/99999')
    assert res.status_code == 404