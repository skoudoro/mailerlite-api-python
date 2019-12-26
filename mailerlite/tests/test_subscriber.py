from mailerlite.subscriber import Subscribers


def test_subscriber():
    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': "fc7b8c5b32067bcd47cafb5f475d2fe9"
    }

    subscriber = Subscribers(headers)

    # res = subscriber.all()
    # print(len(res))
    # res = subscriber.active()
    # print(len(res))
    # res = subscriber.get(email='demo@mailerlite.com')
    # print(res)
    # res = subscriber.get(id='1343965485')
    # print(res)
    # res = subscriber.search(search='demo@mailerlite.com')
    # print(res)
    # res = subscriber.groups(id='1343965485')
    # print(res)
    # res = subscriber.activity(id='1343965485')
    # print(res)
    # Test create
    data = {'name': 'John',
            'email': 'demo-678@mailerlite.com',
            'fields': {'company': 'MailerLite'}
            }
    res = subscriber.create(data)
    print(res)


test_subscriber()
