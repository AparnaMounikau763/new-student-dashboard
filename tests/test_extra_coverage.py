import pytest

# ---------------- REGISTER EDGE ---------------- #

def test_register_missing_all(client):
    res = client.post("/register", json={})
    assert res.status_code == 400


# ---------------- LOGIN EDGE ---------------- #

def test_login_missing_fields(client):
    res = client.post("/login", json={})
    assert res.status_code == 400


# ---------------- SEARCH EDGE ---------------- #

def test_search_no_query(client):
    res = client.get("/search")
    assert res.status_code == 400


# ---------------- STUDENT UPDATE EDGE ---------------- #

def test_update_non_existing_user(client):
    res = client.put("/students/9999", json={"username": "ghost"})
    assert res.status_code == 404


# ---------------- DELETE EDGE ---------------- #

def test_delete_non_existing_user(client):
    res = client.delete("/students/9999")
    assert res.status_code == 404


# ---------------- GET SINGLE EDGE ---------------- #

def test_get_non_existing_user(client):
    res = client.get("/students/9999")
    assert res.status_code == 404