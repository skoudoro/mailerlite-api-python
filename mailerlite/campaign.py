"""Manage Campaign."""

import mailerlite.client as client
from mailerlite.constants import Campaign, Stats


class Campaigns:

    def __init__(self, headers):
        """Initialize Campaigns object.

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

    def all(self, status='sent', limit=100, offset=0, order='asc',
            as_json=False):
        """Get paginated details of all campaigns from your account.

        look at https://developers.mailerlite.com/reference#campaigns-by-type

        Parameters
        ----------
        status : str
            Define campaigns type: Here are the possible values:
            * sent - campaigns which are sent already (default)
            * draft - campaigns which aren't completed or sent to subscribers
            * outbox - campaigns which are being sent right now or scheduled
        limit : int
            How many campaigns you want
        offset : int
            page index
        order : str
            pick the order. Here are the possible values: ASC (default) or DESC
        as_json : bool
            return result as json format

        Returns
        -------
        campaigns: list
            all desired campaign. More informations concerning campaign :
            https://developers.mailerlite.com/reference#section-response-body-parameters
        """
        if order.upper() not in ['ASC', 'DESC']:
            raise IOError("Incorrect order, please choose between ASC or DESC")

        params = {'limit': limit, 'offset': offset, 'order': order}
        url = client.build_url('campaigns', status, **params)
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        for res in res_json:
            res['opened'] = Stats(**res.pop('opened'))
            res['clicked'] = Stats(**res.pop('clicked'))

        all_campaigns = [Campaign(**res) for res in res_json]
        return all_campaigns

    # def get(self, campaign_id, as_json=False):
    #     """ NOT AVAILABLE via API
    # Get a campaigns from your account.

    #     look at https://developers.mailerlite.com/reference#campaigns-by-type

    #     Parameters
    #     ----------
    #     campaign_id : int
    #         should be campaign id. e.g: id=1343965485
    #     as_json : bool
    #         return result as json format
    #     Returns
    #     -------
    #     campaign: :class:`Campaign`
    #         a single campaign
    #     """
    #     url = client.build_url('campaigns', campaign_id)
    #     res_code, res_json = client.get(url, headers=self.headers)

    #     if as_json or not res_json:
    #         return res_json

    #     res_json['opened'] = Stats(**res_json.pop('opened'))
    #     res_json['clicked'] = Stats(**res_json.pop('clicked'))

    #     return Campaign(**res_json)

    def update(self, campaign_id, html, plain, auto_inline=True):
        r"""Upload your HTML template to created campaign.

        https://developers.mailerlite.com/v2/reference#put-custom-content-to-campaign

        Parameters
        ----------
        campaign_id : int
            the campaign id that you want to update
        html : str
            HTML template source
        plain : str
            Plain text of email
        auto_inline : bool, optional
            Defines if it is needed to convert available CSS to inline CSS
            (excluding media queries)

        Returns
        -------
        success : bool

        Examples:
        ---------
        >>> from mailerlite import MailerLiteApi
        >>> api = MailerLiteApi('my_keys')
        >>> html = '<h1>Title</h1><p>Content</p><p><small>'
        >>> html += '<a href=\"{$unsubscribe}\">Unsubscribe</a></small></p>'
        >>> plain = "Your email client does not support HTML emails. "
        >>> plain += "Open newsletter here: {$url}. If you do not want"
        >>> plain += " to receive emails from us, click here: {$unsubscribe}"
        >>> api.campaigns.update(campaign_id, html=html, plain=plain)
        True

        Notes
        -----
        * HTML template must contain a link for unsubscribe. It may look like
            this: <a href="{$unsubscribe}">Unsubscribe</a>
        * Some email clients do not support HTML emails so you need to set
            plain text email and it must contain these variables:
            * {$unsubscribe} - unsubscribe link
            * {$url} - URL to your HTML newsletter
        """
        url = client.build_url('campaigns', campaign_id, 'content')
        # Todo, Check html syntax
        body = {"html": html, "plain": plain}
        _, res_json = client.put(url, body=body, headers=self.headers)

        if not res_json:
            return False

        return res_json['success']

    def create(self, data):
        """Create campaign where you will use your custom HTML template.

        https://developers.mailerlite.com/v2/reference#campaigns

        Parameters
        ----------
        data : dict
            campaign object. For a regular campaign, you  can use the
            following example:
            data = {"subject": "Regular campaign subject",
                    "groups": [2984475, 3237221],
                    "type": "regular"}
            For a/b  campaign type, you need more fields, Here an example:
            data = {"groups": [2984475, 3237221],
                    "type": "ab",
                    "ab_settings": {"send_type": "subject",
                                    "values": ["Email subject A",
                                               "Email subject B"],
                                    "ab_win_type": "opens",
                                    "winner_after": 1,
                                    "winner_after_type": "h",
                                    "split_part": "10"
                                }}

        Returns
        -------
        response : int
            response value
        content : dict
            The JSON output from the API
        """
        if not isinstance(data, dict):
            raise ValueError('In data should be a dictionary.')
        required_keys = ['type', ]
        optional_keys = ['subject', 'from', 'from_name', 'language',
                         'ab_settings']
        ab_settings_keys = ['values', 'send_type', 'ab_win_type',
                            'winner_after', 'winner_after_type',
                            'split_part']
        available_keys = required_keys + optional_keys

        errors = [rk for rk in required_keys if rk not in data.keys()]
        if errors:
            raise ValueError("The following keys are missing and they"
                             " are required : {}".format(errors))

        if ('groups' not in data.keys()) and ('segments' not in data.keys()):
            raise ValueError("'groups' key is required if 'segments' key"
                             " are not specified. If specified, 'groups'"
                             " are ignored")

        unknown_keys = [d for d in data.keys() if d not in available_keys
                        if d not in ['groups', 'segments']]
        if unknown_keys:
            raise ValueError("The following keys are unknown: {}"
                             .format(unknown_keys))

        if 'ab_settings' in data.keys():
            errors = [rk for rk in ab_settings_keys
                      if rk not in data['ab_settings'].keys()]
            if errors:
                raise ValueError("The following keys are missing in the"
                                 " ab_settings and they are required : "
                                 "{}".format(errors))

        url = client.build_url('campaigns')
        return client.post(url, body=data, headers=self.headers)

    def delete(self, campaign_id):
        """Remove a campaign.

        look at https://developers.mailerlite.com/reference#delete-campaign

        Parameters
        ----------
        campaign_id : int
            campaign id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('campaigns', campaign_id)
        return client.delete(url, headers=self.headers)

    def count(self, status='sent'):
        """Return the number of campaigns.

        Returns
        -------
        status : str
            Define campaigns type: Here are the possible values:
            * sent - campaigns which are sent already (default)
            * draft - campaigns which aren't completed or sent to subscribers
            * outbox - campaigns which are being sent right now or scheduled
        count: int
            number of campaigns
        """
        if status.lower() not in ['sent', 'draft', 'outbox']:
            raise ValueError('Incorrect status, check documentation')
        url = client.build_url('campaigns', status.lower(), 'count')
        _, res_json = client.get(url, headers=self.headers)
        return res_json['count']
