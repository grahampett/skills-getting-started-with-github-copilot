import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "anotherstudent@mergington.edu")
])
def test_signup(activity, email):
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()
    # Check participant added
    response2 = client.get("/activities")
    assert email in response2.json()[activity]["participants"]

def test_remove_participant():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Add participant
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 204
    # Check participant removed
    response2 = client.get("/activities")
    assert email not in response2.json()[activity]["participants"]
