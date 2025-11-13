from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_reset_database():
    response = client.get("/reset")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "deleted_count" in json_response


def test_add_email_to_blacklist():
    response = client.post(
        "/blacklists",
        json={
            "email": "spammer@example.com",
            "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "blocked_reason": "Spam sender detected by security team"
        },
        headers={"Authorization": "Bearer my-super-secret-static-token"}
    )
    assert response.status_code == 201
    json_response = response.json()
    assert "message" in json_response


def test_add_email_already_in_blacklist():
    response = client.post(
        "/blacklists",
        json={
            "email": "spammer@example.com",
            "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "blocked_reason": "Spam sender detected by security team"
        },
        headers={"Authorization": "Bearer my-super-secret-static-token"}
    )
    assert response.status_code == 409
    json_response = response.json()
    assert "detail" in json_response


def test_get_email_found_in_blacklist():
    response = client.get(
        "/blacklists/spammer@example.com",
        headers={"Authorization": "Bearer my-super-secret-static-token"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["is_blacklisted"] == True


def test_get_email_not_found_in_blacklist():
    response = client.get(
        "/blacklists/nonexistent@example.com",
        headers={"Authorization": "Bearer my-super-secret-static-token"}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["is_blacklisted"] == False
