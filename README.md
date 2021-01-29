# Mailerlite-api-python

Python Wrapper for Mailerlite API v2

<table align="center">
    <tr>
      <td align="center"><b>Deployment</b></td>
      <td align="center"><a href="https://pypi.org/project/mailerlite-api-python/"><img src="https://img.shields.io/pypi/v/mailerlite-api-python.svg?logo=python&logoColor=white" alt="pypi mailerlite"></a></td>
    </tr>
    <tr>
      <td align="center"><b>Build Status</b></td>
      <td align="center"><a href="https://travis-ci.com/github/skoudoro/mailerlite-api-python"><img src="https://travis-ci.com/skoudoro/mailerlite-api-python.svg?branch=master"></a> <a href="https://github.com/skoudoro/mailerlite-api-python/actions?query=workflow%3A%22CI+%28PIP%29%22"><img src="https://github.com/skoudoro/mailerlite-api-python/workflows/CI%20(PIP)/badge.svg"></a> <a href="https://github.com/skoudoro/mailerlite-api-python/actions?query=workflow%3A%22CI+%28CONDA%29%22"><img src="https://github.com/skoudoro/mailerlite-api-python/workflows/CI%20(CONDA)/badge.svg"></a></td>
    </tr>
    <tr>
      <td align="center"><b>Metrics</b></td>
      <td align="center">
        <a href="https://app.codacy.com/manual/skab12/mailerlite-api-python?utm_source=github.com&utm_medium=referral&utm_content=skoudoro/mailerlite-api-python&utm_campaign=Badge_Grade_Dashboard
"><img src="https://api.codacy.com/project/badge/Grade/9c17e95d29cd489ba86411db969a576e" alt="codacy mailerlite python"></a> <a href="https://codecov.io/gh/skoudoro/mailerlite-api-python"><img src="https://codecov.io/gh/skoudoro/mailerlite-api-python/branch/master/graph/badge.svg" alt="codecov mailerlite python"></a>
      </td>
    </tr>
    <tr>
      <td align="center"><b>License</b></td>
      <td align="center"><a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="bsd"></a></td>
    </tr>
    <tr>
      <td align="center"><b>Community</b></td>
      <td align="center"><a href="https://github.com/skoudoro/mailerlite-api-python/graphs/contributors"><img src="https://img.shields.io/github/contributors/skoudoro/mailerlite-api-python.svg"></a> <a href="https://github.com/skoudoro/mailerlite-api-python/blob/master/CONTRIBUTING.rst"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a> <a href="https://github.com/skoudoro/mailerlite-api-python/blob/master/CONTRIBUTING.rst"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a></td>
    </tr>
</table>

## Getting Started

### Installation

This client is hosted at [PyPi](https://pypi.org/project/mailerlite-api-python/) under the name **mailerlite-api-python**, to install it, simply run

```terminal
pip install mailerlite-api-python
```

or install dev version:

```terminal
git clone https://github.com/skoudoro/mailerlite-api-python.git
pip install -e .
````

## Method reference

For complete reference, visit the [official MailerLite API reference](https://developers.mailerlite.com/reference).

## Examples

### Initialization

First, Grab YOUR_API_KEY from your Mailerlite account (Profile > Integrations > Developer Api).

```python
>>> from mailerlite import MailerLiteApi
>>> api = MailerLiteApi('YOUR_API_KEY')
```

### Campaigns

#### Get all campaigns or a specific one

```python
>>> all_campaigns = api.campaigns.all()
>>> draft = api.compaings.all(status='draft')
```

#### Modify a campaign

```python
>>> one_campaign = all_campaigns[0]
>>> html = '<h1>Title</h1><p>Content</p><p><small><a href=\"{$unsubscribe}\">Unsubscribe</a></small></p>'
>>> plain = "Your email client does not support HTML emails. "
>>> plain += "Open newsletter here: {$url}. If you do not want"
>>> plain += " to receive emails from us, click here: {$unsubscribe}"

>>> api.campaigns.update(one_campaign.id, html=html, plain=plain)
```

#### Create / Delete a campaign

```python
>>> data = {"subject": "Regular campaign subject",
                       "groups": [2984475, 3237221],
                       "type": "regular"}
>>> api.campaign.create(data)
>>> api.campaign.delete(campaign_id=3971635)
```

#### count campaign

```python
>>> api.campaign.count()
>>> api.campaign.count(status='draft')
```

### Subscribers

#### Get all subscribers

```python
>>> api.subscribers.all()
>>> api.subscribers.all(stype='active')
>>> api.subscribers.active()
>>> api.subscribers.unsubscribed()
>>> api.subscribers.bounced()
>>> api.subscribers.junk()
>>> api.subscribers.unconfirmed()
```

#### Get one subscriber

```python
>>> api.subscribers.get(email='demo@mailerlite.com')
>>> api.subscribers.get(id=1343965485)
```

#### search

```python
>>> api.subscribers.search(search='demo@mailerlite.com')
```

#### subscribers groups

```python
>>> api.subscribers.groups(id=1343965485)
```

#### subscribers activity

```python
>>> api.subscribers.activity(id='1343965485')
```

#### Create subscriber

```python
>>> data = {'name': 'John',
            'email': 'demo-678@mailerlite.com',
            'fields': {'company': 'MailerLite'}
            }
>>> api.subscribers.create(data)
```

#### Update subscriber

```python
>>> data = {'name': 'John',
            'fields': {'company': 'MailerLite'}
            }
>>> api.subscribers.update(data, id='1343965485')
```

#### Count subscribers

Get the total count of all subscribers in a single call.

Please, be aware that is not documented in the official API.

```python
>>> api.subscribers.count()
```

### Groups

#### Get all Groups

```python
>>> api.groups.all()
>>> api.groups.all(limit=50)
>>> api.groups.all(offset=10)
>>> api.groups.all(gfilters='My Group')
>>> api.groups.all(group_id=12345)
```

#### Create a Group

```python
>>> api.groups.create(group_id=12345, name='My New Group')
```

#### Rename a Group

```python
>>> api.groups.update(group_id=12345, name='New Name')
```

#### Get a Group

```python
>>> api.groups.get(group_id=12345)
```

#### Delete a Group

```python
>>> api.groups.delete()
>>> api.groups.delete(group_id=12345)
```

#### Get all subscribers in a Group

```python
>>> api.groups.subscribers(group_id=12345)
>>> api.groups.subscribers(group_id=12345, limit=50, offset=1)
>>> api.groups.subscribers(group_id=12345, stype='active')
```

#### Get one subscriber from a Group

```python
>>> api.groups.subscriber(group_id=12345, subscriber_id=54321)
```

#### Add list of subscribers to a Group

This method calls the import endpoint https://developers.mailerlite.com/reference#add-many-subscribers
```python
>>> api.groups.add_subscribers(group_id=12345, subscribers_data=[{"email": "john@wick.com", "name": "John Wick"}], autoresponders=False, resubscribe=False, as_json=False)
```
```subscriber_data``` argument accepts a list of dictionaries or just one dictionary containing the subscriber name and email 

#### Add a single subscriber to a Group

This method calls the add single subscriber endpoint https://developers.mailerlite.com/reference#add-single-subscriber
```python
>>> api.groups.add_single_subscriber(group_id=12345, subscriber_data={"email": "john@wick.com", "name": "John Wick" ...}, autoresponders=False, resubscribe=False, as_json=False)
```
Unlike the method above, this add only one subscriber to a group. The ```subscriber_data``` argument accepts all subscriber attributes.
Check available attributes on https://developers.mailerlite.com/reference#create-a-subscriber

#### Delete one subscriber from a Group

```python
>>> api.groups.delete_subscriber(group_id=12345, subscriber_id=54321)
```

### Segments

#### Get list of Segments

```python
>>> api.segments.all()
```

#### Get count of Segments

```python
>>> api.segments.count()
```

### Fields

#### Get list of Fields

```python
>>> api.fields.all()
```

#### Get one Field

```python
>>> api.fields.get(field_id=123456)
```

#### Create / update / delete one Field

```python
>>> api.fields.create(title="my custom title")
>>> api.fields.update(field_id=123456, title="my new title 2")
>>> api.fields.delete(field_id=123456)
```

### Webhooks

#### Get list of Webhooks

```python
>>> api.webhooks.all()
```

#### Get one webhook

```python
>>> api.webhooks.get(webhook_id=123456)
```

#### Create/update/delete one webhook

```python
>>> api.webhooks.create(url="https://yoursite/script-is-here",
...                     event="subscriber.create")
>>> api.webhooks.update(webhook_id=123456,
...                     url="https://yoursite/script-is-here",
...                     event="subscriber.create")
>>> api.webhooks.delete(webhook_id=123456)
```

### Account

```python
# Get some info or stats
>>> api.account.info()
>>> api.account.stats()
>>> api.account.double_optin()
# Set up the double_optin
>>> api.account.set_double_optin(True)
```

### Batch

```python
>>> batch_requests = {"requests": [{"method":"GET",
...                                 "path": "/api/v2/groups"
...                                 },
...                                 {"method":"POST",
...                                  "path": "/api/v2/groups",
...                                  "body": {"name": "New group"}
...                                 }
...                                 ]
...                    }
>>> api.batch(batch_requests)
```

## Tests

* Step 1: Install pytest

```terminal
  pip install pytest
```

* Step 2: Run the tests

```terminal
  pytest -svv mailerlite
```

## Contribute

We love contributions!

You've discovered a bug or something else you want to change - excellent! [Create an issue](https://github.com/skoudoro/mailerlite-api-python/issues)!

You've worked out a way to fix it – even better! Submit a [Pull Request](https://github.com/skoudoro/mailerlite-api-python/pulls)!

Start with the [contributing guide](https://github.com/skoudoro/mailerlite-api-python/blob/master/CONTRIBUTING.rst)!

## License

Project under 3-clause BSD license, more informations [here](https://github.com/skoudoro/mailerlite-api-python/blob/master/LICENSE)
