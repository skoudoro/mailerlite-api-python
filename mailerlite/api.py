from mailerlite.campaign import Campaigns
from mailerlite.segment import Segments
from mailerlite.subscriber import Subscribers
from mailerlite.group import Groups
from mailerlite.field import Fields


class MailerLiteApi:
    """
    Python interface to the mailerlite v1 API.

    """

    def __init__(self, api_key):
        """Initialize a new mailerlite.api object.

        Parameters
        ----------
        api_key : str
            Your mailerlite api_key.
        """
        if not api_key:
            raise ValueError("Empty API_KEY. Please enter a valid API_KEY")

        self.headers = {'content-type': "application/json",
                        'x-mailerlite-apikey': api_key
                        }

        self.campaigns = Campaigns(headers=self.headers)
        self.segments = Segments(headers=self.headers)
        self.subscribers = Subscribers(headers=self.headers)
        self.groups = Groups(headers=self.headers)
        self.fields = Fields(headers=self.headers)
