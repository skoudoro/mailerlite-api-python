from mailerlite.campaign import Campaigns
from mailerlite import MailerLiteApi
from mailerlite.constants import API_KEY_TEST
import requests


CAMPAIN_ID = None

def test_basic_campaign():
    url = "https://api.mailerlite.com/api/v2/subscribers"

    data = {'name': 'John',
            'email': 'demo@mailerlite.com',
            'fields': {'company': 'MailerLite'}
            }

    # payload = json.dumps(data)

    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': API_KEY_TEST
    }

    response = requests.request("GET", url, headers=headers)

    # print(response.text)


def test_create_campaign():
    global CAMPAIN_ID
    test_key = API_KEY_TEST
    api = MailerLiteApi(test_key)
    data = {"subject": "Regular campaign subject",
            "groups": [2984475, 3237221],
            "type": "regular"}
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
    code, res = api.campaigns.create(data)
    CAMPAIN_ID = res['id']
    assert code == 200
    code, res = api.campaigns.create(data_ab)
    assert code == 200
    assert isinstance(res, dict)


def test_update_campaign():
    global CAMPAIN_ID
    test_key = API_KEY_TEST
    api = MailerLiteApi(test_key)

    html = '<h1>Title</h1><p>Content</p><p><small>'
    html += '<a href=\"{$unsubscribe}\">Unsubscribe</a></small></p>'
    plain = "Your email client does not support HTML emails. "
    plain += "Open newsletter here: {$url}. If you do not want"
    plain += " to receive emails from us, click here: {$unsubscribe}"
    code, res = api.campaigns.update(CAMPAIN_ID, html=html, plain=plain)
    assert code == 200
    assert isinstance(res, dict)


def test_campaign():
    # my_key = ""
    test_key = API_KEY_TEST
    api = MailerLiteApi(test_key)

    _ = api.campaigns.all()
    # seg, meta = api.segments.all()
    # sub = api.subscribers
    # print(sub.search())
    # print(sub.search(search='demo@mailerlite.com'))
