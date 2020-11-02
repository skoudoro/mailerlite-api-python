"""Module to test Account class."""

import pytest

from mailerlite.account import Account
from mailerlite.constants import API_KEY_TEST


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


def test_wrong_headers():
    headers_2 = {'content-type': "application/json",
                 'x-mailerlite-apikey': 'FAKE_KEY'
                 }
    headers_3 = {'content-type': "application/json",
                 }
    headers_4 = {'x-mailerlite-apikey': 'FAKE_KEY'
                 }

    with pytest.raises(OSError):
        acc = Account(headers_2)
        acc.info()

    with pytest.raises(ValueError):
        acc = Account(headers_3)

    with pytest.raises(ValueError):
        acc = Account(headers_4)


def test_account(header):
    acc = Account(header)

    info = acc.info()
    assert 'account' in info.keys()

    stats = acc.stats()
    assert 'subscribed' in stats.keys()
    assert 'unsubscribed' in stats.keys()
    assert stats.get('subscribed') > stats.get('unsubscribed')

    optin = acc.double_optin()
    assert 'enabled' in optin.keys()
