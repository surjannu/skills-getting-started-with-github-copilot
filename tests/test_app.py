"""Tests for the FastAPI backend application."""

from urllib.parse import quote


def test_get_activities(client):
    """Test GET /activities returns all activities."""
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "Chess Club" in data
    # Check that Chess Club has the expected structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_signup_for_activity_success(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Basketball Team"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_for_activity_duplicate(client):
    """Test signup fails when student is already signed up."""
    # Arrange
    activity_name = "Tennis Club"
    email = "duplicate@example.com"
    # First signup
    client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Act - try to signup again
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_for_activity_not_found(client):
    """Test signup fails for non-existent activity."""
    # Arrange
    activity_name = "nonexistent"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_remove_participant_success(client):
    """Test successful removal of a participant."""
    # Arrange
    activity_name = "Painting Class"
    email = "remove@example.com"
    # First signup
    client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_remove_participant_not_signed_up(client):
    """Test removal fails when participant is not signed up."""
    # Arrange
    activity_name = "Sculpture Workshop"
    email = "notsigned@example.com"

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_remove_participant_activity_not_found(client):
    """Test removal fails for non-existent activity."""
    # Arrange
    activity_name = "nonexistent"
    email = "test@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect(client):
    """Test GET / redirects to static index."""
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"