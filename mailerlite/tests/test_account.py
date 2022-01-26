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


def test_wrong_headers(header):
    # test valid first
    try:
        _ = Account(header)
    except ValueError:
        return

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
    try:
        acc = Account(header)
    except ValueError:
        return

    info = acc.info()
    assert 'account' in info.keys()

    stats = acc.stats()
    assert 'subscribed' in stats.keys()
    assert 'unsubscribed' in stats.keys()
    assert stats.get('subscribed') > stats.get('unsubscribed')

    optin = acc.double_optin()
    assert 'enabled' in optin.keys()

    with pytest.raises(OSError):
        # double_optin not available with this API keys
        acc.set_double_optin(False)
