"""Manage Campaign."""

from collections import namedtuple
import mailerlite.client as client

Stats = namedtuple('Stats', ['count', 'rate'])
Campaign = namedtuple('Campaign', ['id', 'total_recipients', 'type',
                                   'date_created', 'date_send', 'name',
                                   'status', 'opened', 'clicked'])


class Campaigns:

    def __init__(self, headers):
        """Initialize Campaigns object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

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
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        for res in res_json:
            res['opened'] = Stats(**res.pop('opened'))
            res['clicked'] = Stats(**res.pop('clicked'))

        all_campaigns = [Campaign(**res) for res in res_json]
        return all_campaigns

    # def get(self, ):
    #     """Get paginated details of all campaigns from your account.

    #     look at https://developers.mailerlite.com/reference#campaigns-by-type

    #     Parameters
    #     ----------
    #     Returns
    #     -------
    #     campaigns: list
    #         all desired campaign
    #     """
    #     pass

    # def update(self):
    #     pass

    # def create(self):
    #     pass

    def delete(self, id):
        """Remove a campaign.

        look at https://developers.mailerlite.com/reference#delete-campaign

        Parameters
        ----------
        id : int
            campaign id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('campaigns', id)
        return client.delete(url, headers=self.headers)

    @property
    def count(self):
        """Return the number of campaigns.

        Returns
        -------
        count: int
            number of campaigns
        """
        url = client.build_url('campaigns', 'count')
        res_code, res_json = client.get(url, headers=self.headers)
        return res_json['count']
