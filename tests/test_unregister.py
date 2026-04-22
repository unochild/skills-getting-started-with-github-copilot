from urllib.parse import quote

import src.app as app_module


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_rejects_non_registered_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student not registered for this activity"
