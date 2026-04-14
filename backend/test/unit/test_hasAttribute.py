import pytest
from src.util.helpers import hasAttribute

@pytest.fixture
def obj():
    return {"name": "Jane Doe"}

@pytest.mark.unit
def test_hasAttribute(obj):
    result = hasAttribute(obj, "name")
    assert result == True

@pytest.mark.unit
def test_hasAttribute_false(obj):
    result = hasAttribute(obj, "age")
    assert result == False

# def test_hasAttribute_false(obj):
#     result = hasAttribute(obj, 'email')
#     assert result == False

# @pytest.mark.unit
# def test_hasAttribute_none():
#     # my_dict = None
#     result = hasAttribute(None, "name")
#     # print(result)
#     assert result == False

