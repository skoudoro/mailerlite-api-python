"""Module to tests Webhook."""

import pytest

from mailerlite.constants import API_KEY_TEST, Webhook
from mailerlite.webhook import Webhooks


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
        wh = Webhooks(headers_2)
        wh.all()

    with pytest.raises(ValueError):
        wh = Webhooks(headers_3)

    with pytest.raises(ValueError):
        wh = Webhooks(headers_4)


def test_webhook_error(header):
    wh = Webhooks(header)

    with pytest.raises(OSError):
        wh.update(123456, "new_url", "new_event")


def test_webhook_crud(header):
    wh = Webhooks(header)
    all_wh = wh.all()

    assert len(all_wh) > 0
    assert len(all_wh) == wh.count()

    first_wh = all_wh[0]
    current_wh = wh.get(first_wh.id)

    # assert isinstance(current_wh, Webhook)
    for f in current_wh._fields:
        assert current_wh._asdict().get(f) == first_wh._asdict().get(f)

    # Need to Find a free webhooks tools for unittest
    # import ipdb; ipdb.set_trace()
    # code, custom_wh = wh.create(first_wh.url, first_wh.event)
    # assert code in [200, 201]

    # import ipdb; ipdb.set_trace()
    # assert custom_wh.event == first_wh.event
    # assert custom_wh.url == first_wh.url
    # assert custom_wh.id != first_wh.id
