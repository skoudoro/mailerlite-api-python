# Mailerlite-api-python

![](https://img.shields.io/travis/skoudoro/mailerlite-api-python.svg?target=https://travis-ci.org/skoudoro/mailerlite-api-python)
![](https://img.shields.io/pypi/v/mailerlite-api-python.svg?target=https://pypi.python.org/pypi/mailerlite-api-python)


Python Wrapper for Mailerlite API v2


# Getting Started

## Installation

This client is hosted at PyPi under the name mailerlite-api-python, to install it, simply run

```
pip install mailerlite-api-python
```

## Examples

### Initialization

First, Grab YOUR_API_KEY from your Mailerlite account (Profile > Integrations > Developer Api).

```python
from mailerlite import MailerLiteApi

api = MailerLiteApi('YOUR_API_KEY')
```

### Campaigns

#### Get all campaigns or a specific one

```python
all_campaigns = api.campaigns.all()
draft = api.compaings.all(status='draft')
```

#### Modify a campaign

```python
one_campaign = all_campaigns[0]
html = '<h1>Title</h1><p>Content</p><p><small><a href=\"{$unsubscribe}\">Unsubscribe</a></small></p>'
plain = "Your email client does not support HTML emails. "
plain += "Open newsletter here: {$url}. If you do not want"
plain += " to receive emails from us, click here: {$unsubscribe}"

api.campaigns.update(one_campaign.id, html=html, plain=plain)
```

#### Create /Delete a campaign

```python
data = {"subject": "Regular campaign subject",
                   "groups": [2984475, 3237221],
                   "type": "regular"}
api.campaign.create(data)
api.campaign.delete(campaign_id=3971635)
```

#### count campaign

```python
api.campaign.count()
api.campaign.count(status='draft')
```

### Subscribers

#### Get all subscribers

```python
api.subscribers.all()
api.subscribers.all(stype='active')
api.subscribers.active()
```

#### Get one subscriber

```python
api.subscribers.get(email='demo@mailerlite.com')
api.subscriber.get(id=1343965485)
```

#### search

```python
api.subscriber.search(search='demo@mailerlite.com')
```

#### subscribers groups

```python
api.subscriber.groups(id=1343965485)
```

#### subscribers activity

```python
subscriber.activity(id='1343965485')
```

#### Create subscriber

```python
data = {'name': 'John',
        'email': 'demo-678@mailerlite.com',
        'fields': {'company': 'MailerLite'}
        }
api.subscriber.create(data)
```

### Groups

Need documentation...

### Segments

##### Get list of Segments.

```python
api.segments.all()
```

##### Get countof  Segments.

```python
api.segments.count()
```

### Fields

##### Get list of Fields.

```python
api.fields.all()
```

##### Get one Field

```python
api.fields.get(field_id=123456)
```

##### Create/update/delete one Field

```python
api.fields.create(title="my custom title")
api.fields.update(field_id=123456, title="my new title 2")
api.fields.delete(field_id=123456)
```

### Webhooks

##### Get list of Webhooks.

```python
api.webhooks.all()
```

##### Get one webhook

```python
api.webhooks.get(webhook_id=123456)
```

##### Create/update/delete one webhook

```python
api.webhooks.create(url="https://yoursite/script-is-here",
	                event="subscriber.create")
api.webhooks.update(webhook_id=123456,
                    url="https://yoursite/script-is-here",
	                event="subscriber.create")
api.webhooks.delete(webhook_id=123456)
```

### Account

```python
# Get some info or stats
api.account.info()
api.account.stats()
api.account.double_optin()
# Set up the double_optin
api.account.set_double_optin(True)
```

### Batch

```python
batch_requests = {"requests": [{"method":"GET",
                                "path": "/api/v2/groups"
                                },
                                {"method":"POST",
                                    "path": "/api/v2/groups",
                                "body": {"name": "New group"}
                                }
                                ]
                   }
api.batch(batch_requests)
```

# Contribute

We love contributions!

You've discovered a bug or something else you want to change - excellent! [Create an issue](https://github.com/skoudoro/mailerlite-api-python/issues)!

You've worked out a way to fix it – even better! Submit a [Pull Request](https://github.com/skoudoro/mailerlite-api-python/pulls)!

Start with the [contributing guide](https://github.com/skoudoro/mailerlite-api-python/blob/master/CONTRIBUTING.rst)!

# License

Project under 3-clause BSD license, more informations [here](https://github.com/skoudoro/mailerlite-api-python/blob/master/LICENSE)

