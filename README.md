# mailerlite-api-python

![](https://img.shields.io/travis/skoudoro/mailerlite-api-python.svg?target=https://travis-ci.org/skoudoro/mailerlite-api-python)
![](https://img.shields.io/pypi/v/mailerlite-api-python.svg?target=https://pypi.python.org/pypi/mailerlite-api-python)


Python Wrapper for Mailerlite API v2


# Getting Started

## Installation

This client is hosted at PyPi under the name mailerlite-api-python, to install it, simply run

pip install mailerlite-api-python

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
#### Create a campaign
```python
data = {"subject": "Regular campaign subject",
                   "groups": [2984475, 3237221],
                   "type": "regular"}
api.campaign.create(data)
```

### Subscribers


### Groups

### Segments

### Fields

### Webhooks

### Account

### Batch

# Contribute

We love contributions!

You've discovered a bug or something else you want to change - excellent! Create an issue!

You've worked out a way to fix it – even better! Submit a Pull Request!

Start with the contributing guide!


# Support

If you are having issues, please [let us know](https://github.com/skoudoro/mailerlite-api-python/issues) or submit a [pull request](https://github.com/skoudoro/mailerlite-api-python/pulls).

# License

Project under 3-clause BSD license, more informations [here](https://github.com/skoudoro/mailerlite-api-python/blob/master/LICENSE)

