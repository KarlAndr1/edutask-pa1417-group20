import pytest

from unittest.mock import Mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    dao_mock = Mock()
    return dao_mock

@pytest.mark.unit
def test_get_user_by_email_valid_single(mock_dao):
    # Setup
    user_controller = UserController(dao=mock_dao)
    email = "user@example.com"
    mock_dao.find.return_value = [{"email": email, "name": "Test User"}]

    # Execution
    user = user_controller.get_user_by_email(email)

    # Assertion
    assert user == {"email": email, "name": "Test User"}

@pytest.mark.unit
def test_get_user_by_email_valid_multiple(mock_dao, capsys):
    # Setup
    user_controller = UserController(dao=mock_dao)
    email = "user@example.com"
    mock_dao.find.return_value = [
        {"email": email, "name": "Test User 1"},
        {"email": email, "name": "Test User 2"}
    ]

    # Execution
    user = user_controller.get_user_by_email(email)
    captured = capsys.readouterr()

    # Assertion
    assert (user == {"email": email, "name": "Test User 1"} and 
            "more than one user found with mail" in captured.out)

@pytest.mark.unit
def test_get_user_by_email_invalid_format(mock_dao):
    # Setup
    user_controller = UserController(dao=mock_dao)
    email = "invalid_email_format"
	
    # Execution and Assertion
    with pytest.raises(ValueError):
        user_controller.get_user_by_email(email)

@pytest.mark.unit
def test_get_user_by_email_non_existent(mock_dao):
    # Setup
    user_controller = UserController(dao=mock_dao)
    email = "nonexistent@example.com"
    mock_dao.find.return_value = []

    # Execution
    user = user_controller.get_user_by_email(email)

    # Assertion
    assert user is None

@pytest.mark.unit
def test_get_user_by_email_database_error(mock_dao):
    # Setup
    user_controller = UserController(dao=mock_dao)
    email = "user@example.com"
    mock_dao.find.side_effect = Exception("Database error")

    # Execution and Assertion
    with pytest.raises(Exception) as excinfo:
        user_controller.get_user_by_email(email)
    assert "Database error" in str(excinfo.value)
