from urllib.parse import quote

import src.app as app_module


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup", params={"email": existing_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
