"""Module to tests groups."""

import pytest

from mailerlite.constants import API_KEY_TEST, Group
from mailerlite.group import Groups


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


def test_groups_instance(header):
    with pytest.raises(ValueError):
        Groups(API_KEY_TEST)

    groups = Groups(header)
    res_json = groups.all(as_json=True)

    # TEST to check if there is new key in the API
    missing_keys = []
    for g in res_json:
        for k in g.keys():
            if not hasattr(Group, k):
                missing_keys.append(k)

    missing_keys = set(missing_keys)
    error_msg = "The following keys are unkown: {}, ".format(missing_keys)
    error_msg += "please update API"
    assert not missing_keys, error_msg

    # Test to check if is group object is valid
    res = groups.all()
    assert len(res) > 0
    for g in res:
        assert isinstance(g, Group)


def test_groups_crud(header):
    groups = Groups(header)

    expected_group_name = "TEST_K_GROUP"
    expected_group_name_2 = "TEST_GROUP_KKK"
    e_res = groups.create(expected_group_name)
    assert e_res.name == expected_group_name

    res = groups.get(e_res.id)
    assert res.name == expected_group_name

    groups.update(e_res.id, expected_group_name_2)
    res = groups.get(e_res.id)
    assert res.name == expected_group_name_2

    assert groups.delete(e_res.id)

    with pytest.raises(OSError):
        groups.get(e_res.id)


def test_groups_subscriber():
    # groups = Groups(header)

    # subs = groups.subscriber
    pass
