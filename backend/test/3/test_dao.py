import pytest
from unittest.mock import patch, Mock

from src.util.dao import DAO

from pymongo.errors import WriteError

test_schema = {
	"$jsonSchema": {
		"bsonType": "object",
		"required": ["name", "description"],
		"properties": {
			"name": {
				"bsonType": "string",
				"uniqueItems": True
			},
			"description": {
				"bsonType": "string"
			},
			"optBool": {
				"bsonType": "bool"
			}
		}
	}
}

"""
	Testing DAO. Creates a temporary collection with a known schema
"""
@pytest.fixture
def TDAO():
	with patch('src.util.dao.getValidator', autospec=True) as getValidator:
		getValidator.return_value = test_schema
		d = DAO("__testing_collection")
	
	yield d
	
	d.drop()

def test_create_valid_object(TDAO):
	
	created = TDAO.create({
		"name": "test",
		"description": "testing"
	})
	found = TDAO.find()
	
	assert "_id" in created
	assert created["name"] == "test"
	assert created["description"] == "testing"
		
	assert len(found) == 1
	assert found[0] == created

def test_create_object_with_missing_property(TDAO):
	with pytest.raises(WriteError):
		TDAO.create({"name": "test"})
	
	found = TDAO.find()
	
	assert len(found) == 0

def test_create_object_with_invalid_type(TDAO):
	with pytest.raises(WriteError):
		TDAO.create({"name": "test", "description": "testing", "optBool": "A string"})

	found = TDAO.find()
	
	assert len(found) == 0

def test_create_objects_with_unique_properties(TDAO):
	first = TDAO.create({"name": "test1", "description": "testing"})
	second = TDAO.create({"name": "test2", "description": "testing"})
	
	found = TDAO.find()
	assert len(found) == 2
	assert first in found
	assert second in found

def test_create_objects_with_duplicate_unique_properties(TDAO):
	created = TDAO.create({"name": "test", "description": "testing"})
	with pytest.raises(WriteError):
		TDAO.create({"name": "test", "description": "testing"})
	
	found = TDAO.find()
	assert len(found) == 1
	assert found[0] == created
	
