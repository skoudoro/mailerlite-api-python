"""Module to tests Field."""
import random
import string

import pytest

from mailerlite.constants import API_KEY_TEST, Field
from mailerlite.field import Fields


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


def generate_random_string(length, seed=1234567):
    random.seed(seed)
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def test_wrong_headers():
    headers_1 = {'content-type': "app",
                 'x-mailerlite-apikey': API_KEY_TEST
                 }
    headers_2 = {'content-type': "application/json",
                 'x-mailerlite-apikey': 'FAKE_KEY'
                 }
    headers_3 = {'content-type': "application/json",
                 }
    headers_4 = {'x-mailerlite-apikey': 'FAKE_KEY'
                 }

    with pytest.raises(OSError):
        field = Fields(headers_1)
        field.create("field_new", "TEXT")

    with pytest.raises(OSError):
        field = Fields(headers_2)
        field.create("field_new", "TEXT")

    with pytest.raises(ValueError):
        field = Fields(headers_3)

    with pytest.raises(ValueError):
        field = Fields(headers_4)


def test_fields_error(header):
    fields = Fields(header)

    # Unknown keys
    with pytest.raises(ValueError):
        fields.create("field_name", "UNKNOW_FIELD")

    with pytest.raises(OSError):
        fields.update(123456, "new_title")


def test_fields_crud(header):
    fields = Fields(header)
    all_fields = fields.all()

    assert len(all_fields) > 0

    last_field = all_fields[-2]
    current_field = fields.get(last_field.id)

    assert isinstance(current_field, Field)
    for f in current_field._fields:
        assert current_field._asdict().get(f) == last_field._asdict().get(f)

    field_name = "TEST_"
    field_name += generate_random_string(random.randint(5, 15))
    code, custom_fields = fields.create(field_name, 'TEXT')
    assert code in [200, 201]

    custom_fields = Field(**custom_fields)
    assert custom_fields.title == field_name
    assert custom_fields.key == field_name.lower()
    assert custom_fields.type == 'TEXT'

    updated = fields.update(custom_fields.id, "TEST_MAILERLITE_PYTHON")
    assert updated.title == 'TEST_MAILERLITE_PYTHON'
    assert updated.key == custom_fields.key
    assert updated.type == custom_fields.type

    assert fields.delete(updated.id) is None
    assert fields.get(updated.id) is None
