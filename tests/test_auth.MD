def test_root(app_client):
    resp = app_client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "API de autenticação funcionando!"}

def test_register_success(app_client):
    payload = {
        "email": "user1@example.com",
        "password": "StrongPass123!",
        "password_confirmation": "StrongPass123!",
        "user_type": "aluno",
    }
    resp = app_client.post("/users/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["user_type"] == payload["user_type"]
    assert "id" in data and "created_at" in data and "updated_at" in data
    assert "hashed_password" not in data

def test_register_duplicate_email(app_client):
    payload = {
        "email": "dup@example.com",
        "password": "StrongPass123!",
        "password_confirmation": "StrongPass123!",
        "user_type": "professor",
    }
    resp1 = app_client.post("/users/register", json=payload)
    assert resp1.status_code == 201
    resp2 = app_client.post("/users/register", json=payload)
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Email já está cadastrado."

def test_register_password_mismatch(app_client):
    payload = {
        "email": "mismatch@example.com",
        "password": "StrongPass123!",
        "password_confirmation": "StrongPassDIFF!",
        "user_type": "mentor",
    }
    resp = app_client.post("/users/register", json=payload)
    assert resp.status_code == 422

def test_login_success(app_client):
    email = "login_ok@example.com"
    password = "Secret123!"
    reg = app_client.post("/users/register", json={
        "email": email,
        "password": password,
        "password_confirmation": password,
        "user_type": "pesquisador",
    })
    assert reg.status_code == 201

    resp = app_client.post(
        "/auth/token",
        data={"username": email, "password": password},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_login_invalid_password(app_client):
    email = "login_badpass@example.com"
    password = "RightPass1!"
    reg = app_client.post("/users/register", json={
        "email": email,
        "password": password,
        "password_confirmation": password,
        "user_type": "aluno",
    })
    assert reg.status_code == 201

    resp = app_client.post(
        "/auth/token",
        data={"username": email, "password": "WrongPass!"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Email ou senha inválidos."

def test_login_nonexistent_user(app_client):
    resp = app_client.post(
        "/auth/token",
        data={"username": "ghost@example.com", "password": "AnyPass1!"},
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Email ou senha inválidos."