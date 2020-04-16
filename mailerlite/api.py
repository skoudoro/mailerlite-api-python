"""Mailerlite API."""

from mailerlite.campaign import Campaigns
from mailerlite.segment import Segments
from mailerlite.subscriber import Subscribers
from mailerlite.group import Groups
from mailerlite.field import Fields
from mailerlite.webhook import Webhooks
from mailerlite.account import Account
import mailerlite.client as client


class MailerLiteApi:
    """Python interface to the mailerlite v2 API.

    """

    def __init__(self, api_key):
        """Initialize a new mailerlite.api object.

        Parameters
        ----------
        api_key : str
            Your mailerlite api_key.

        """
        if not api_key or not isinstance(api_key, str):
            raise ValueError("Empty API_KEY. Please enter a valid API_KEY")

        self._headers = {'content-type': "application/json",
                         'x-mailerlite-apikey': api_key
                         }

        self.campaigns = Campaigns(headers=self.headers)
        self.segments = Segments(headers=self.headers)
        self.subscribers = Subscribers(headers=self.headers)
        self.groups = Groups(headers=self.headers)
        self.fields = Fields(headers=self.headers)
        self.webhooks = Webhooks(headers=self.headers)
        self.account = Account(headers=self.headers)

    @property
    def headers(self):
        return self._headers

    def batch(self, batch_requests):
        """Execute a list of command. Dedicated for experts.

        https://developers.mailerlite.com/v2/reference#batch-api-requests

        Parameters
        ----------
        batch_requests : list of dict
            all you command. E.g:
            batch_requests = {"requests": [{"method":"GET",
                                            "path": "/api/v2/groups"
                                            },
                                            {"method":"POST",
                                             "path": "/api/v2/groups",
                                            "body": {"name": "New group"}
                                           }
                                          ]
                               }

        Returns
        -------
        results : list
            list of all desired object

        Notes
        -----
        * There is a limit of maximum 50 requests per single batch.
        * The order of response objects are the same as sent requests.
        * requests parameter should not be empty

        """
        url = client.build_url('batch')
        return client.post(url, body=batch_requests, headers=self.headers)
