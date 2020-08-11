"""Manage Subcribers."""

from warnings import warn
import mailerlite.client as client
from mailerlite.constants import Subscriber, Activity, Group, Field


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
        valid_headers, error_msg = client.check_headers(headers)
        if not valid_headers:
            raise ValueError(error_msg)

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
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        for res in res_json:
            res['fields'] = [Field(**field) for field in res['fields']]

        all_subscribers = [Subscriber(**res) for res in res_json]
        return all_subscribers

    def count(self, stype=None, as_json=False):
        """Get the count of subscribers of a type.

        Please, be aware that `count` is not documented in the official API
        https://developers.mailerlite.com/reference#subscribers

        Parameters
        ----------
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
        number: Integer
            the count of subscribers
        """
        warn("Please, be aware that `count` is not in the official API")

        params = {}
        if stype and stype.lower() in ['active', 'unsubscribed', 'bounced',
                                       'junk', 'unconfirmed']:
            params.update({'type': stype})

        url = client.build_url('subscribers', 'count', **params)
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return res_json['count']

    def get(self, as_json=False, **identifier):
        """Get a single subscriber from your account.

        https://developers.mailerlite.com/v2/reference#single-subscriber

        Parameters
        ----------
        identifier : str
            should be subscriber id or email.
            e.g: id=1343965485 or email='demo@mailerlite.com'
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
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        res_json['fields'] = [Field(**res) for res in res_json['fields']]

        return Subscriber(**res_json)

    def delete(self, subscriber_id):
        """Remove a subscribers.

        Parameters
        ----------
        subscriber_id : int
            subscribers id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('subscribers', subscriber_id)
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

        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        if not minimized:
            for res in res_json:
                res['fields'] = [Field(**field) for field in res['fields']]

        all_subscribers = [Subscriber(**res) for res in res_json]
        return all_subscribers

    def groups(self, as_json=False, **identifier):
        """Get groups subscriber belongs to.

        More informations:
        https://developers.mailerlite.com/v2/reference#groups-subscriber-belongs-to

        Parameters
        ----------
        identifier : str
            should be subscriber id or email.
            e.g: id=1343965485 or email='demo@mailerlite.com'
        as_json : bool
            return result as json format

        Returns
        -------
        groups: list
            all groups that a subscriber belongs to. More informations :
            https://developers.mailerlite.com/v2/reference#groups
        """
        path = get_id_or_email_identifier(**identifier)
        if path is None:
            raise IOError('An identifier must be define')

        url = client.build_url('subscribers', path, 'groups')

        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        all_groups = [Group(**res) for res in res_json]
        return all_groups

    def activity(self, as_json=False, atype=None, **identifier):
        """Get activities (clicks, opens, etc) of selected subscriber.

        More informations:
        https://developers.mailerlite.com/v2/reference#activity-of-single-subscriber

        Parameters
        ----------
        identifier : str
            should be subscriber id or email.
            e.g: id=1343965485 or email='demo@mailerlite.com'
        as_json : bool
            return result as json format
        atype : str
            Define activity type: Here are the possible values:
            * None - All activities (default)
            * opens
            * clicks
            * bounces
            * junks
            * unsubscribes
            * forwards
            * sendings

        Returns
        -------
        activities: list
            all subscriber activities. More informations :
            https://developers.mailerlite.com/v2/reference#activity-of-single-subscriber
        """
        path = get_id_or_email_identifier(**identifier)
        if path is None:
            raise IOError('An identifier must be define')

        args = ['subscribers', path, 'activity']
        if atype:
            possible_atype = ['opens', 'clicks', 'junks', 'bounces',
                              'unsubscribes', 'forwards', 'sendings']
            if atype not in possible_atype:
                raise ValueError('Incorrect value atype. Activity type should'
                                 ' be {0}'.format(possible_atype))
            args.append(atype)

        url = client.build_url(*args)

        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        all_activities = [Activity(**res) for res in res_json]
        return all_activities

    def update(self, data, as_json=False, **identifier):
        """Update single subscriber.

        https://developers.mailerlite.com/v2/reference#update-subscriber

        Parameters
        ----------
        data : dict
            subscriber object. only the email is required.
            you can use the following example:
            data = {'name'   : 'John',
                    'fields' : {'company': 'MailerLite'}
                    }
        as_json : bool
            return result as json format
        identifier : str
            should be subscriber id or email.
            e.g: id=1343965485 or email='demo@mailerlite.com'

        Returns
        -------
        response : int
            response value
        content : dict
            The JSON output from the API

        Notes
        -----
        The email of a subscriber can not be updated

        """
        path = get_id_or_email_identifier(**identifier)
        if path is None:
            raise IOError('An identifier must be define')

        if 'email' in data.keys():
            raise ValueError("Subscriber email can not be updated. Please, "
                             "remove this field or create a new Subscriber. "
                             "For more informations, look at "
                             "http://help.mailerlite.com/article/show"
                             "/29233-how-to-edit-a-subscribers-data")

        optional_keys = ['name', 'type', 'fields', 'resend_autoresponders']
        unknown_keys = [d for d in data.keys() if d not in optional_keys
                        if d not in ['groups', 'segments']]
        if unknown_keys:
            raise ValueError("The following keys are unknown: {}"
                             .format(unknown_keys))

        url = client.build_url('subscribers', path)
        _, res_json = client.put(url, body=data, headers=self.headers)

        if as_json or not res_json:
            return res_json

        res_json['fields'] = [Field(**res) for res in res_json['fields']]

        return Subscriber(**res_json)

    def create(self, data, as_json=False):
        """Add new single subscriber.

        https://developers.mailerlite.com/v2/reference#create-a-subscriber

        Parameters
        ----------
        data : dict
            subscriber object. only the email is required.
            you can use the following example:
            data = {'name'   : 'John',
                    'email'  : 'demo@mailerlite.com',
                    'fields' : {'company': 'MailerLite'}
                    }
        as_json : bool
            return result as json format
        Returns
        -------
        subscriber: :class:Subscriber
            a single subscriber
        """
        if not isinstance(data, dict):
            raise ValueError('In data should be a dictionary.')
        required_keys = ['email', ]
        optional_keys = ['name', 'fields', 'resubscribe', 'type',
                         'signup_ip', 'signup_timestamp', 'confirmation_ip',
                         'confirmation_timestamp']
        available_keys = required_keys + optional_keys

        errors = [rk for rk in required_keys if rk not in data.keys()]
        if errors:
            raise ValueError("The following keys are missing and they"
                             " are required : {}".format(errors))

        unknown_keys = [d for d in data.keys() if d not in available_keys
                        if d not in ['groups', 'segments']]
        if unknown_keys:
            raise ValueError("The following keys are unknown: {}"
                             .format(unknown_keys))

        url = client.build_url('subscribers')
        _, res_json = client.post(url, body=data, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Subscriber(**res_json)
