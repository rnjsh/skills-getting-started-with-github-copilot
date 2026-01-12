import urllib.parse

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # expect at least one known activity
    assert "Soccer Team" in data


def test_signup_and_unregister():
    activity = "Soccer Team"
    email = "testuser@example.com"

    # Clean up if already present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}")

    # Sign up
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify presence
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify absence
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
