from src.app import activities


class TestActivitiesAPI:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activity_names = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Basketball Team", "Drama Club", "Art Studio", "Math Olympiad", "Science Club"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        payload = response.json()
        assert set(payload.keys()) == expected_activity_names
        assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

    def test_signup_for_activity_adds_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]

    def test_signup_for_duplicate_participant_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Student is already signed up for this activity"}

    def test_signup_for_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Unknown Activity"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    def test_unregister_participant_removes_email_from_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
        assert email not in activities[activity_name]["participants"]

    def test_unregister_unknown_participant_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": "Student is not signed up for this activity"}
