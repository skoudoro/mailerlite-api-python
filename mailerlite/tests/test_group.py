"""Module to tests groups."""
import random
import string
import time

import pytest

from mailerlite.constants import API_KEY_TEST, Group
from mailerlite.group import Groups


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


def generate_random_email(length, seed=1234567):
    random.seed(seed)
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    mail = 'demo-test-{}-{}@mailerlite.com'.format(result_str, seed)
    return mail


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


def test_groups_subscriber(header):
    groups = Groups(header)

    n_groups = groups.all()
    assert len(n_groups) > 0
    group_1 = n_groups[0]

    subs_in_group_1 = groups.subscribers(group_1.id)
    assert len(subs_in_group_1) > 0

    sub1 = subs_in_group_1[0]
    tmp_sub = groups.subscriber(group_1.id, sub1.id)

    assert sub1.email == tmp_sub.email

    while True:
        try:
            num = random.randint(1000, 100000)
            mail = generate_random_email(length=15, seed=num)
            data = {'name': 'John',
                    'email': mail,
                    'fields': {'company': 'MailerLite'}
                    }
            new_subs = groups.add_subscribers(group_1.id, data)
        except OSError:
            time.sleep(3)
        else:
            break

    print(new_subs)
    if new_subs:
        assert new_subs[0].email == mail

        groups.delete_subscriber(group_1.id, new_subs[0].id)


def test_groups_single_subscriber(header):
    groups = Groups(header)

    n_groups = groups.all()
    assert len(n_groups) > 0
    group_1 = n_groups[0]

    subs_in_group_1 = groups.subscribers(group_1.id)
    assert len(subs_in_group_1) > 0

    sub1 = subs_in_group_1[0]
    tmp_sub = groups.subscriber(group_1.id, sub1.id)

    assert sub1.email == tmp_sub.email

    while True:
        try:
            num = random.randint(1000, 100000)
            mail = generate_random_email(length=15, seed=num)
            data = {'name': 'John',
                    'email': mail,
                    'fields': {'company': 'MailerLite'}
                    }
            new_sub = groups.add_single_subscriber(group_1.id, data)
        except OSError:
            time.sleep(3)
        else:
            break

    print(new_sub)
    if new_sub:
        assert new_sub.email == mail

        groups.delete_subscriber(group_1.id, new_sub.id)
