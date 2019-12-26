import mailerlite.client as client


def test_build_url():
    res = client.build_url('test', 125)
    assert res == 'test/125'

    res = client.build_url('test', 125, id='my_id')
    assert res == 'test/125?id=my_id'

    res = client.build_url('test', 125, id='my_id', value=123)
    assert res == 'test/125?id=my_id&value=123'


test_build_url()
