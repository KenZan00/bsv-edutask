import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.util.dao import DAO
from pymongo.errors import WriteError


validation_structure = { "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
                "description": "the first name of a user must be determined"
            }, 
            "lastName": {
                "bsonType": "string",
                "description": "the last name of a user must be determined"
            },
            "email": {
                "bsonType": "string",
                "description": "the email address of a user must be determined",
                "uniqueItems": True
            },
            "tasks": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }}


# As testers, we viewed this as a fully testable NONE production database.
@pytest.fixture
def db_sut():
    with patch("src.util.dao.getValidator") as mock_get_validator:
        mock_get_validator.return_value = validation_structure
        database = DAO('user')

        database.collection.delete_many({})

        yield database

        database.collection.delete_many({})


# Test create document with a valid structure.
@pytest.mark.integration
def test_create_document_valid(db_sut):


    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": "test@test.com"
    }

    result = db_sut.create(document)

    assert result is not None
    assert "_id" in result


# Missing required field, raise exception.
@pytest.mark.integration
def test_create_document_not_required_input_email(db_sut):

    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        # No email
    }
    
    with pytest.raises(WriteError):
        db_sut.create(document)


# Testing wrong data format, integer instead of string as specified by validator
@pytest.mark.integration
def test_create_document_wrong_datatype(db_sut):
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": 757
    }
    
    with pytest.raises(WriteError):
        db_sut.create(document)

# Testing duplciate unique item, which should raise an exception according to the documentation of dao.py -> create() method
# The test will fail, that is not how validation work in MongoDB, this test is tho show a defiency in the cods documentation and implementation.
@pytest.mark.integration
def test_create_document_unique_item_constraint(db_sut):
    
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": "unique.email@test.com"
    }

    db_sut.create(document)
    
    with pytest.raises(WriteError):
        db_sut.create(document)



# Removed options and empty document as it would either trigger the same WriteError på validation or
# get validated and inputed per option if other requirements are still in place.