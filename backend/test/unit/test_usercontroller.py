import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

# Code updated for Lab 1 by suggestions from the lab instructions.
# Arrange - Act - Assert technique. The database is mocked in fixture with a return of UserController to reduce cod
# All test are sorted in same order as Lab 1 step 4 Relevant tests.

# Added dao and usercontroller to avoid repetition in code.
@pytest.fixture
def user_controller():
    dao_mock = MagicMock()
    return UserController(dao_mock)

# Test for no user found with the email.
def test_user_by_email_none(user_controller):
    user_controller.dao.find.return_value = []
    res = user_controller.get_user_by_email("emmaill@emilsson.se")

    assert res is None

#  Tests for 1 valid user
def test_user_by_email_valid(user_controller):
    user_controller.dao.find.return_value = [{"email": "emmaill@emilsson.se"}]
    res = user_controller.get_user_by_email("emmaill@emilsson.se")
    assert res == {"email": "emmaill@emilsson.se"}

# Test for multiple users with same email, returns the first user.
def test_get_user_multiple(user_controller):
    user_controller.dao.find.return_value = [{"id": 1, "email": "123@test.com"}, {"id": 2, "email": "123@test.com"}]
    result = user_controller.get_user_by_email("123@test.com")

    assert result == {"id": 1, "email": "123@test.com"}

# Test database exception
def test_dao_exception(user_controller):
    user_controller.dao.find.side_effect = Exception

    with pytest.raises(Exception):
        user_controller.get_user_by_email("emmaill@emilsson.se")

# Test for invalid email format.
def test_get_user_invalid_email(user_controller):

    with pytest.raises(ValueError):
        user_controller.get_user_by_email("wrongtest.com")