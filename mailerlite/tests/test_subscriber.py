"""Module to test subscriber class."""
import random
import string
import time

import pytest

from mailerlite.constants import API_KEY_TEST
from mailerlite.subscriber import Subscribers


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


def test_wrong_headers():
    headers_2 = {'content-type': "application/json",
                 'x-mailerlite-apikey': 'FAKE_KEY'
                 }
    headers_3 = {'content-type': "application/json",
                 }
    headers_4 = {'x-mailerlite-apikey': 'FAKE_KEY'
                 }

    with pytest.raises(OSError):
        subs = Subscribers(headers_2)
        subs.all()

    with pytest.raises(ValueError):
        subs = Subscribers(headers_3)

    with pytest.raises(ValueError):
        subs = Subscribers(headers_4)


def test_subscribers_error(header):
    subs = Subscribers(header)

    # Unknown keys
    with pytest.raises(ValueError):
        subs.create("field_name")

    with pytest.raises(ValueError):
        subs.create({'mail': 'demo-test-12345555@mailerlite.com'})

    with pytest.raises(ValueError):
        subs.create({'email': 'demo-test-12345555@mailerlite.com',
                     'group': 12345
                     })

    with pytest.raises(OSError):
        subs.update(123456, "new_title")

    with pytest.raises(OSError):
        subs.get(mail='demo-test-12345555@mailerlite.com')


def test_subscribers_crud(header):
    subscriber = Subscribers(header)

    while True:
        try:
            num = random.randint(1000, 100000)
            mail = generate_random_email(length=15, seed=num)
            data = {'name': 'John',
                    'email': mail,
                    'fields': {'company': 'MailerLite'}
                    }
            e_res = subscriber.create(data)
        except OSError:
            time.sleep(3)
        else:
            break

    res = subscriber.get(email=mail)
    assert e_res.email == res.email

    res = subscriber.get(id=e_res.id)
    assert e_res.email == res.email

    res = subscriber.get(email=mail, as_json=True)
    assert e_res.email == res['email']

    res = subscriber.search(search=mail)
    assert len(res) > 0
    assert e_res.email == res[0].email

    with pytest.raises(IOError):
        subscriber.update({'email': 'new@mail.com'})

    with pytest.raises(IOError):
        subscriber.update({'email': 'new@mail.com'}, e_res.id)

    with pytest.raises(ValueError):
        subscriber.update({'email': 'new@mail.com'}, id=e_res.id)

    with pytest.raises(ValueError):
        subscriber.update({'random': 'new@mail.com'}, id=e_res.id)

    subscriber.update({'name': 'Jack'}, id=e_res.id)
    res = subscriber.get(id=e_res.id)
    assert e_res.name != res.name
    assert res.name == 'Jack'

    res = subscriber.active()
    assert len(res) > 0
    res = subscriber.unsubscribed()
    assert len(res) > 0
    res = subscriber.bounced()
    assert len(res) > 0
    res = subscriber.unconfirmed()
    assert len(res) > 0
    res = subscriber.junk()
    assert len(res) >= 0
    res = subscriber.all(as_json=True)
    assert len(res) > 0

    assert subscriber.count() == subscriber.count(as_json=True).get('count')

    groups = subscriber.groups(email=mail)
    assert len(groups) in [0, 1]

    activity = subscriber.activity(email=mail)
    assert len(activity) in [0, 1]

    assert subscriber.delete(e_res.id) is None
