from mailerlite.group import Groups
from mailerlite.constants import API_KEY_TEST, Group


def test_groups():
    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': API_KEY_TEST
    }

    groups = Groups(headers)
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
