"""Module to test client."""
import mailerlite.client as client
from mailerlite.constants import API_KEY_TEST


def test_build_url():
    res = client.build_url('test', 125)
    assert res == 'test/125'

    res = client.build_url('test', 125, id='my_id')
    assert res == 'test/125?id=my_id'

    res = client.build_url('test', 125, id='my_id', value=123)
    assert res == 'test/125?id=my_id&value=123'


def test_check_headers():

    for headers in [{}, None, [], (), 0, '']:
        res, msg = client.check_headers(headers)
        assert not res
        assert "empty headers" in msg.lower()

    for headers in [['content-type'], ('content-type'), 1, 'content-type']:
        res, msg = client.check_headers(headers)
        assert not res
        assert "headers should be a dictionnary" in msg.lower()

    d1 = {'content-type': '', }
    d2 = {'x-mailerlite-apikey': '', }
    for headers in [d1, d2]:
        res, msg = client.check_headers(headers)
        assert not res
        assert "'content-type' and 'x-mailerlite-apikey'" in msg.lower()

    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': API_KEY_TEST
    }

    res, msg = client.check_headers(headers)
    assert res
    assert not msg
