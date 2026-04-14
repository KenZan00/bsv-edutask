import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


def test_user_by_email_valid():
    # Arrange
    mocked_dao = MagicMock()
    mocked_dao.find.return_value = [{"email": "emmaill@emilsson.se"}]
    controller = UserController(mocked_dao)
    # Act
    res = controller.get_user_by_email("emmaill@emilsson.se")
    # Assert
    assert res == {"email": "emmaill@emilsson.se"}

def test_get_user_invalid_email():
    mock_service = MagicMock()
    controller = UserController(mock_service)

    with pytest.raises(ValueError):
        controller.get_user_by_email("wrongtest.com")

def test_user_by_email_none():
    mocked_dao = MagicMock()
    mocked_dao.find.return_value = []
    controller = UserController(mocked_dao)
    res = controller.get_user_by_email("emmaill@emilsson.se")

    assert res is None

def test_get_user_multiple():
    mock_service = MagicMock()
    mock_service.find.return_value = [{"id": 1, "email": "123@test.com"}, {"id": 2, "email": "123@test.com"}]

    controller = UserController(mock_service)
    result = controller.get_user_by_email("123@test.com")
    assert result == {"id": 1, "email": "123@test.com"}

def test_dao_exception():
    mock_dao = MagicMock()
    mock_dao.find.side_effect = Exception
    controller = UserController(mock_dao)

    with pytest.raises(Exception):
        controller.get_user_by_email("emmaill@emilsson.se")