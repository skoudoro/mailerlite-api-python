"""Manage Webhooks."""

import mailerlite.client as client


class Webhooks:

    def __init__(self, headers):
        """Initialize Webhooks object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def all(self):
        """Get list of Webhooks.

        https://developers.mailerlite.com/v2/reference#get-webhooks-list

        Returns
        -------
        webhooks: list of dict
            all webhooks.
        """
        url = client.build_url('webhooks')
        res_code, res_json = client.get(url, headers=self.headers)

        return res_json

    def get(self, webhook_id):
        """Get single field by ID from your account.

        https://developers.mailerlite.com/v2/reference#get-single-webhook

        Parameters
        ----------
        webhook_id : int
            ID of a webhook

        Returns
        -------
        webhook: dict
            the desired webhook.
        """
        url = client.build_url('webhooks', webhook_id)
        res_code, res_json = client.get(url, headers=self.headers)

        return res_json

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
        field : :class:Field
            field object updated
        """
        url = client.build_url('webhooks', webhook_id)
        body = {"url": url, 'event': event}
        res_code, res_json = client.put(url, body=body, headers=self.headers)

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
        res_code, res_json = client.post(url, body=body, headers=self.headers)

        return res_json
