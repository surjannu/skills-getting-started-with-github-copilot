import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module


@pytest.fixture
def client():
    """Fixture to provide a TestClient for the FastAPI app with isolated activities state."""
    original_activities = copy.deepcopy(app_module.activities)
    yield TestClient(app)
    app_module.activities.clear()
    app_module.activities.update(original_activities)