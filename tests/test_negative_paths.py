import uuid

def test_register_duplicate_email(client):
    uid = str(uuid.uuid4())[:8]
    data = {
        "username": f"user_{uid}",
        "email": f"{uid}@mail.com",
        "password": "123"
    }

    client.post("/register", json=data)
    res = client.post("/register", json=data)

    assert res.status_code == 400


def test_login_invalid_user(client):
    res = client.post("/login", json={
        "email": "nouser@mail.com",
        "password": "123"
    })
    assert res.status_code == 401


def test_get_invalid_student(client):
    res = client.get("/student/9999")
    assert res.status_code == 404


def test_update_invalid_student(client):
    res = client.put("/student/9999", json={"username": "x"})
    assert res.status_code == 404


def test_delete_invalid_student(client):
    res = client.delete("/student/9999")
    assert res.status_code == 404


def test_search_no_results(client):
    res = client.get("/search?username=doesnotexist")
    assert res.status_code == 404


def test_system_check(client):
    res = client.get("/system-check")
    assert res.status_code == 200
    assert "ok" in res.get_data(as_text=True)