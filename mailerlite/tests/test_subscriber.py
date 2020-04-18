"""Module to test subscriber class."""
import pytest
from random import randint

from mailerlite.subscriber import Subscribers
from mailerlite.constants import API_KEY_TEST


def test_subscriber():
    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': API_KEY_TEST
    }

    with pytest.raises(ValueError):
        Subscribers(API_KEY_TEST)

    subscriber = Subscribers(headers)

    num = randint(0, 1000)
    mail = 'demo-test-{}@mailerlite.com'.format(num)
    data = {'name': 'John',
            'email': mail,
            'fields': {'company': 'MailerLite'}
            }

    e_res = subscriber.create(data)
    res = subscriber.get(email=mail)
    assert e_res.email == res.email

    res = subscriber.get(id=e_res.id)
    assert e_res.email == res.email

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

    # res = subscriber.groups(id='1343965485')
    # print(res)
    # res = subscriber.activity(id='1343965485')
    # print(res)
