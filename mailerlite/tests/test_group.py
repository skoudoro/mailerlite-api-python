"""Module to tests groups."""
from mailerlite.group import Groups
from mailerlite.constants import API_KEY_TEST, Group
import pytest
import responses

@pytest.fixture
def groups():
    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': API_KEY_TEST
    }

    return Groups(headers)

def test_groups_instance(groups):
    with pytest.raises(ValueError):
        Groups(API_KEY_TEST)

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


def test_groups_crud(groups):
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

@responses.activate
def test_get_group_using_valid_id_returns_a_group(groups):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://api.mailerlite.com/api/v2/groups/1234',
                 body="""{
                    "id": 3640549,
                    "name": "My Group",
                    "total": 1,
                    "active": 1,
                    "unsubscribed": 0,
                    "bounced": 0,
                    "unconfirmed": 0,
                    "junk": 0,
                    "sent": 23,
                    "opened": 7,
                    "clicked": 3,
                    "date_created": "2016-04-04 11:02:33",
                    "date_updated": "2016-04-04 11:02:33"
                }""", status=200,
                 content_type='application/json')
    
        res = groups.get(1234)
        assert isinstance(res, Group)
        assert res.id == 3640549
        assert res.name == "My Group"    
        assert res.total == 1
        assert res.active == 1        
        assert res.unsubscribed == 0
        assert res.bounced == 0
        assert res.unconfirmed == 0
        assert res.junk == 0
        assert res.sent == 23
        assert res.opened == 7
        assert res.clicked == 3

@responses.activate
def test_get_group_using_valid_id_and_json_returns_json(groups):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://api.mailerlite.com/api/v2/groups/1234',
                 body="""{
    "id": 3640549,
    "name": "My Group",
    "total": 1,
    "active": 1,
    "unsubscribed": 0,
    "bounced": 0,
    "unconfirmed": 0,
    "junk": 0,
    "sent": 23,
    "opened": 7,
    "clicked": 3,
    "date_created": "2016-04-04 11:02:33",
    "date_updated": "2016-04-04 11:02:33"
}""", 
                 status=200,
                 content_type='application/json')
    
        res = groups.get(1234, as_json=True)
        assert isinstance(res, dict)
        assert res['id'] == 3640549
        assert res['name'] == "My Group"
        

@responses.activate
def test_get_group_using_invalid_id_returns_not_found(groups):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://api.mailerlite.com/api/v2/groups/1234',
                 body="""{
  "error": {
    "code": 123,
    "message": "Group not found"
  }
}""", status=404,
                 content_type='application/json')
    
        with pytest.raises(IOError):
            groups.get(1234)

def test_groups_subscriber():
    pass
