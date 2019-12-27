"""Get Account information."""

import mailerlite.client as client


class Account:

    def __init__(self, headers):
        """Initialize Account object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def info(self):
        """Get account info.

        https://developers.mailerlite.com/v2/reference#account

        Returns
        -------
        info: dict
            all account information.
        """
        url = client.build_url('me')
        res_code, res_json = client.get(url, headers=self.headers)

        return res_json

    def stats(self):
        """Get basic stats for of account, such as subscribers,
        open/click rates and so on.

        https://developers.mailerlite.com/v2/reference#stats

        Returns
        -------
        stats: dict
            account stats
        """
        url = client.build_url('stats')
        res_code, res_json = client.get(url, headers=self.headers)

        return res_json

    def double_optin(self):
        """Retrieve the status if double opt-in for API and
        integrations is enabled

        https://developers.mailerlite.com/v2/reference#get-double-optin-status

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('settings', 'double_optin')
        res_code, res_json = client.get(url, headers=self.headers)
        return res_json

    def set_double_optin(self, enable):
        """Enable/disabled double opt-in for API and integrations.

        https://developers.mailerlite.com/v2/reference#change-double-optin-status

        Parameters
        ----------
        enable : bool
            status

        Returns
        -------
        status : dict
            action result
        """
        url = client.build_url('settings', 'double_optin')
        body = {'enable': enable}
        res_code, res_json = client.post(url, body=body, headers=self.headers)

        return res_json
