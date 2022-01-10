"""Module to tests Campaign."""
import pytest

from mailerlite.campaign import Campaigns
from mailerlite.constants import API_KEY_TEST
from mailerlite.testing import succeed_or_skip_sensitive_tests


@pytest.fixture
def header():
    headers = {'content-type': "application/json",
               "X-MailerLite-ApiDocs": "true",
               'x-mailerlite-apikey': API_KEY_TEST
               }
    return headers


@pytest.fixture
def campaign_data():
    data = {"subject": "Regular campaign subject",
            "name": "Regular campaign name",
            "groups": [2984475, 3237221],
            "type": "regular"
            }
    return data


@pytest.fixture
def campaign_data_ab():
    data_ab = {"groups": [2984475, 3237221],
               "type": "ab",
               "ab_settings": {"send_type": "subject",
                               "values": ["Email subject A",
                                          "Email subject B"],
                               "ab_win_type": "opens",
                               "winner_after": 1,
                               "winner_after_type": "h",
                               "split_part": "10"
                               }
               }
    return data_ab


def test_wrong_headers(campaign_data):
    headers_1 = {'content-type': "app",
                 "X-MailerLite-ApiDocs": "true",
                 'x-mailerlite-apikey': API_KEY_TEST
                 }
    headers_2 = {'content-type': "application/json",
                 "X-MailerLite-ApiDocs": "true",
                 'x-mailerlite-apikey': 'FAKE_KEY'
                 }
    headers_3 = {'content-type': "application/json",
                 }
    headers_4 = {'x-mailerlite-apikey': 'FAKE_KEY'
                 }

    with pytest.raises(OSError):
        campaign = Campaigns(headers_1)
        campaign.create(campaign_data)

    with pytest.raises(OSError):
        campaign = Campaigns(headers_2)
        campaign.create(campaign_data)

    with pytest.raises(ValueError):
        campaign = Campaigns(headers_3)

    with pytest.raises(ValueError):
        campaign = Campaigns(headers_4)


def test_campaign_error(header):
    campaign = Campaigns(header)

    with pytest.raises(ValueError):
        campaign.count(status='inbox')

    with pytest.raises(IOError):
        campaign.all(order='inbox')

    with pytest.raises(ValueError):
        campaign.create(data=[("subject", "Regular campaign subject"),
                              ("type", "regular")])

    with pytest.raises(ValueError):
        campaign.create(data={"random_keys": "test"})

    with pytest.raises(ValueError):
        campaign.create(data={"random_keys": "test",
                              "type": "regular"})


def test_crud_campaign(header, campaign_data, campaign_data_ab):
    campaign_obj = Campaigns(header)

    code, res = campaign_obj.create(campaign_data)
    assert code == 200

    code, res = campaign_obj.create(campaign_data_ab)
    assert code == 200
    assert isinstance(res, dict)

    html = '<head></head><body><h1>Title</h1><p>Content</p><p><small>'
    html += '<a href=\"{$unsubscribe}\">Unsubscribe</a></small></p></body>'
    plain = "Your email client does not support HTML emails. "
    plain += "Open newsletter here: {$url}. If you do not want"
    plain += " to receive emails from us, click here: {$unsubscribe}"

    updated = campaign_obj.update(res['id'], html=html, plain=plain)
    assert updated
    assert isinstance(updated, bool)

    code, res = campaign_obj.delete(res['id'])
    assert code == 200
    assert res['success']

    res = campaign_obj.all(status='draft', limit=1000)
    nb_draft = campaign_obj.count('draft')
    assert nb_draft > 0
    assert len(res) > 0


@succeed_or_skip_sensitive_tests
def test_create_and_send_campaign(header, campaign_data):
    campaign_obj = Campaigns(header)

    code, res = campaign_obj.create(campaign_data)
    assert code == 200

    html = '<head></head><body><h1>Title</h1><p>Content</p><p><small>'
    html += '<a href=\"{$unsubscribe}\">Unsubscribe</a></small></p></body>'
    plain = "Your email client does not support HTML emails. "
    plain += "Open newsletter here: {$url}. If you do not want"
    plain += " to receive emails from us, click here: {$unsubscribe}"

    updated = campaign_obj.update(res['id'], html=html, plain=plain)

    code, res = campaign_obj.send(res['id'])
    assert code == 200


@succeed_or_skip_sensitive_tests
def test_cancel_send_campaign(header):
    campaign_obj = Campaigns(header)

    if campaign_obj.count('outbox'):
        res = campaign_obj.all(status='outbox', limit=10)
        if not res:
            pytest.skip("No campaign found with outbox status")

        assert res[0].status == 'outbox'
        try:
            code, res_2 = campaign_obj.cancel(res[0].id)
        except OSError:
            pytest.skip("Campaign Not Found so can not be cancel")
        assert code == 200
        assert res_2["status"] == 'draft'
        assert res[0].id == res_2["id"]
