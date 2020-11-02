"""Module to test API class."""

import pytest

from mailerlite import MailerLiteApi
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

    with pytest.raises(ValueError):
        api = MailerLiteApi(headers_2)

    with pytest.raises(OSError):
        api = MailerLiteApi('FAKE_KEY')
        api.subscribers.all()


def test_api(header):
    api = MailerLiteApi(API_KEY_TEST)

    assert api.headers == header

    batch_requests = {"requests": [{"method": "GET",
                                    "path": "/api/v2/groups"
                                    },
                                   {"method": "GET",
                                    "path": "/api/v2/fields"
                                    }
                                   ]
                      }
    res = api.batch(batch_requests)
    assert len(res) == 2
