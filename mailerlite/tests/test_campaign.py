from mailerlite import MailerLiteApi
import requests

def test_basic_campaign():
    url = "https://api.mailerlite.com/api/v2/subscribers"

    data = {
        'name'   : 'John',
        'email'  : 'demo@mailerlite.com',
        'fields' : {'company': 'MailerLite'}
    }

    # payload = json.dumps(data)

    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': "617a44553b28d5b7cdd488b9c2f5facc"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

def test_campaign():
    # my_key = "617a44553b28d5b7cdd488b9c2f5facc"
    test_key = "fc7b8c5b32067bcd47cafb5f475d2fe9"
    api = MailerLiteApi(test_key)

    # c = api.campaigns.all()
    # seg, meta = api.segments.all()
    sub = api.subscribers
    # print(sub.search())
    # print(sub.search(search='demo@mailerlite.com'))
    import ipdb; ipdb.set_trace()


# test_basic_campaign()
test_campaign()
