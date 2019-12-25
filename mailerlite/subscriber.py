"""Manage Subcribers."""

from collections import namedtuple
import mailerlite.client as client

Field = namedtuple('Field', ['key', 'value', 'type'])
Subscriber = namedtuple('Subscriber', ['id', 'name', 'email', 'sent',
                                       'opened', 'clicked', 'type',
                                       'signup_ip', 'signup_timestamp',
                                       'confirmation_ip',
                                       'confirmation_timestamp',
                                       'fields', 'date_subscribe',
                                       'date_unsubscribe', 'date_created',
                                       'date_updated', 'opened_rate',
                                       'clicked_rate', 'country_id'
                                       ])
for nt in [Subscriber, Field]:
    nt.__new__.__defaults__ = (None,) * len(nt._fields)


def get_id_or_email_identifier(**kwargs):
    """Return id or email identifier."""
    identifier = None
    for k in ['id', 'email']:
        identifier = kwargs.get(k, None)
        if identifier is not None:
            break
    return identifier


class Subscribers:

    def __init__(self, headers):
        """Initialize Subscribers object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def active(self, limit=100, offset=0, as_json=False):
        """Get all active Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all active Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        return self.all(limit=limit, offset=offset, stype='active',
                        as_json=as_json)

    def unsubscribed(self, limit=100, offset=0, as_json=False):
        """Get all unsubscribed Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all unsubscribed Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        return self.all(limit=limit, offset=offset, stype='unsubscribed',
                        as_json=as_json)

    def bounced(self, limit=100, offset=0, as_json=False):
        """Get all bounced Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all bounced Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        return self.all(limit=limit, offset=offset, stype='bounced',
                        as_json=as_json)

    def junk(self, limit=100, offset=0, as_json=False):
        """Get all junk Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all junk Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        return self.all(limit=limit, offset=offset, stype='junk',
                        as_json=as_json)

    def unconfirmed(self, limit=100, offset=0, as_json=False):
        """Get all unconfirmed Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all unconfirmed Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        return self.all(limit=limit, offset=offset, stype='unconfirmed',
                        as_json=as_json)

    def all(self, limit=100, offset=0, stype=None, as_json=False):
        """Get paginated details of all Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        limit : int
            How many subscribers you want
        offset : int
            page index
        stype : str
            Define subscriber type: Here are the possible values:
            * None - All subscribers (default)
            * active
            * unsubscribed
            * bounced
            * junk
            * unconfirmed
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all desired Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        params = {'limit': limit, 'offset': offset}
        if stype and stype.lower() in ['active', 'unsubscribed', 'bounced',
                                       'junk', 'unconfirmed']:
            params.update({'type': stype})

        url = client.build_url('subscribers', **params)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        for res in res_json:
            res['fields'] = [Field(**field) for field in res['fields']]

        all_subscribers = [Subscriber(**res) for res in res_json]
        return all_subscribers

    def get(self, as_json=False, **identifier):
        """Get a single subscriber from your account.

        look at https://developers.mailerlite.com/v2/reference#single-subscriber

        Parameters
        ----------
        identifier : str
            should be subscriber id or email.
            e.g: id='1343965485' or email='demo@mailerlite.com'
        as_json : bool
            return result as json format
        Returns
        -------
        subscriber: :class:Subscriber
            a single subscriber
        """
        path = get_id_or_email_identifier(**identifier)
        if path is None:
            raise IOError('An identifier must be define')

        url = client.build_url('subscribers', path)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json:
            return res_json

        res_json['fields'] = [Field(**res) for res in res_json['fields']]

        return Subscriber(**res_json)

    def delete(self, id):
        """Remove a subscribers.

        Parameters
        ----------
        id : int
            subscribers id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('subscribers', id)
        return client.delete(url, headers=self.headers)

    def search(self, search=None, limit=100, offset=0, minimized=True,
               as_json=False):
        """Get paginated details of all Subscribers from your account.

        look at https://developers.mailerlite.com/v2/reference#subscribers

        Parameters
        ----------
        search : str
            query parameter to search
        limit : int
            How many subscribers you want
        offset : int
            page index
        minimized : bool
            return minimized response with: id, email, type
            default: True
        as_json : bool
            return result as json format

        Returns
        -------
        subscribers: list
            all desired Subscribers. More informations :
            https://developers.mailerlite.com/v2/reference#subscribers
        """
        params = {'limit': limit, 'offset': offset, 'minimized': minimized}
        if search is not None:
            params.update({'query': search})
        url = client.build_url('subscribers', 'search', **params)

        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        if not minimized:
            for res in res_json:
                res['fields'] = [Field(**field) for field in res['fields']]

        all_subscribers = [Subscriber(**res) for res in res_json]
        return all_subscribers


    # def update(self):
    #     pass

    # def create(self):
    #     pass
