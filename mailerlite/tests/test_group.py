from mailerlite.group import Groups


def test_groups():
    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': "fc7b8c5b32067bcd47cafb5f475d2fe9"
    }

    groups = Groups(headers)
    res = groups.all()
    print(res)

if __name__ == "__main__":
    test_groups()
