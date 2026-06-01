import pytest
from src.models.request import RequestStatus, Priority

class TestRequestStatus:
    def test_statuses(self):
        assert RequestStatus.DRAFT.value == "draft"
        assert RequestStatus.COMPLETED.value == "completed"
        assert len(RequestStatus) == 10

class TestPriority:
    def test_values(self):
        assert Priority.LOW.value == "low"
        assert Priority.CRITICAL.value == "critical"

class TestValidators:
    def test_email(self):
        from src.utils.validators import validate_email
        assert validate_email("test@example.com") is True
        assert validate_email("invalid") is False

    def test_citizen_id(self):
        from src.utils.validators import validate_citizen_id
        assert validate_citizen_id("1234567890123456") is True
        assert validate_citizen_id("12345") is False

    def test_password(self):
        from src.utils.validators import validate_password_strength
        assert len(validate_password_strength("weak")) > 0
        assert len(validate_password_strength("StrongPass123")) == 0
