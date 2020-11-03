"""Manage Webhooks."""

import mailerlite.client as client
from mailerlite.constants import Webhook


class Webhooks:

    def __init__(self, headers):
        """Initialize Webhooks object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        valid_headers, error_msg = client.check_headers(headers)
        if not valid_headers:
            raise ValueError(error_msg)

        self.headers = headers

    def all(self, as_json=False):
        """Get list of Webhooks.

        https://developers.mailerlite.com/v2/reference#get-webhooks-list

        Returns
        -------
        webhooks: list of dict
            all webhooks.
        as_json : bool
            return result as json format

        """
        url = client.build_url('webhooks')
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        all_webhooks = [Webhook(**res) for res in res_json.get('webhooks')]
        return all_webhooks

    def get(self, webhook_id, as_json=False):
        """Get single field by ID from your account.

        https://developers.mailerlite.com/v2/reference#get-single-webhook

        Parameters
        ----------
        webhook_id : int
            ID of a webhook
        as_json : bool
            return result as json format

        Returns
        -------
        webhook: dict
            the desired webhook.

        """
        url = client.build_url('webhooks', webhook_id)
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        webhook = Webhook(**res_json)
        return webhook

    def delete(self, webhook_id):
        """Remove a webhook.

        https://developers.mailerlite.com/v2/reference#delete-a-webhook

        Parameters
        ----------
        webhook_id : int
            ID of a webhook

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('webhooks', webhook_id)
        return client.delete(url, headers=self.headers)

    def update(self, webhook_id, url, event):
        """Update webhook.

        https://developers.mailerlite.com/v2/reference#update-a-webhook

        Parameters
        ----------
        webhook_id : int
            ID of a webhook
        url : str
            Your URL where callbacks are sent
        event : str
            Subscribed event

        Returns
        -------
        webhook : :class:Webhook
            webhook object updated
        """
        url = client.build_url('webhooks', webhook_id)
        body = {"url": url, 'event': event}
        _, res_json = client.put(url, body=body, headers=self.headers)

        return res_json

    def create(self, url, event):
        """Create a webhook.

        https://developers.mailerlite.com/v2/reference#create-a-webhook

        Parameters
        ----------
        url : str
            Your URL where callbacks are sent
        event : str
            Subscribed event

        Returns
        -------
        field : :class:Field
            field object updated
        """
        url = client.build_url('webhooks')
        body = {"url": url, 'event': event}
        code, res_json = client.post(url, body=body, headers=self.headers)

        webhook = Webhook(**res_json)
        return code, webhook

    def count(self):
        """Return the number of webhooks.

        Returns
        -------
        count: int
            number of webhooks

        """
        res_json = self.all(as_json=True)
        return res_json.get('count') or len(res_json.get('webhooks'))
