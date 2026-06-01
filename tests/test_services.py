import pytest
from src.models.request import RequestStatus
from src.services.workflow import workflow_service, VALID_TRANSITIONS

class TestWorkflowService:
    def test_valid_transitions(self):
        assert workflow_service.validate_transition(RequestStatus.DRAFT, RequestStatus.SUBMITTED) is True
        assert workflow_service.validate_transition(RequestStatus.SUBMITTED, RequestStatus.UNDER_REVIEW) is True

    def test_invalid_transitions(self):
        assert workflow_service.validate_transition(RequestStatus.DRAFT, RequestStatus.COMPLETED) is False
        assert workflow_service.validate_transition(RequestStatus.COMPLETED, RequestStatus.IN_PROGRESS) is False

    def test_terminal_states(self):
        assert VALID_TRANSITIONS[RequestStatus.COMPLETED] == []
        assert VALID_TRANSITIONS[RequestStatus.REJECTED] == []

    def test_all_states_have_transitions(self):
        for status in RequestStatus:
            assert status in VALID_TRANSITIONS
