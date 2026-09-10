from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a TestClient with a fresh in-memory activity store for each test."""
    original_activities = deepcopy(activities)

    try:
        activities.clear()
        activities.update(deepcopy(original_activities))

        with TestClient(app) as test_client:
            yield test_client
    finally:
        activities.clear()
        activities.update(deepcopy(original_activities))
