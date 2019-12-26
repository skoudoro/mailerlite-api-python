"""Manage Groups."""

import mailerlite.client as client
from mailerlite.constants import Subscriber, Group, Field


class Groups:

    def __init__(self, headers):
        """Initialize Groups object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def all(self, limit=100, offset=0, gfilters='', as_json=False):
        """Get list of groups from your account.

        look at https://developers.mailerlite.com/v2/reference#groups

        Parameters
        ----------
        limit : int
            How many groups you want
        offset : int
            page index
        gfilters : str
            group filters
        as_json : bool
            return result as json format

        Returns
        -------
        groups: list
            all desired Groups. More informations :
            https://developers.mailerlite.com/v2/reference#groups
        """
        params = {'limit': limit, 'offset': offset, 'filters': gfilters}
        url = client.build_url('groups', **params)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        all_groups = [Group(**res) for res in res_json]
        return all_groups

    def get(self, id, as_json=False):
        """Get single group by ID from your account.

        look at https://developers.mailerlite.com/v2/reference#single-group

        Parameters
        ----------
        id : int
            should be group id. e.g: id=1343965485
        as_json : bool
            return result as json format
        Returns
        -------
        Group: :class:Group
            a single group
        """
        url = client.build_url('groups', id)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Group(**res_json)

    def delete(self, id):
        """Remove a group.

        https://developers.mailerlite.com/v2/reference#delete-group

        Parameters
        ----------
        id : int
            group id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('groups', id)
        return client.delete(url, headers=self.headers)

    def update(self, group_id, name, as_json=False):
        """Update existing group.

        https://developers.mailerlite.com/v2/reference#rename-group

        Parameters
        ----------
        group_id : int
            group that you want to rename
        name : str
            group name
        as_json : bool
            return result as json format
        Returns
        -------
        group: :class:Group
            group object
        """
        url = client.build_url('groups', group_id)
        body = {"name": name, }
        res_code, res_json = client.put(url, body=body, headers=self.headers)

        if not res_json:
            return False

        return Group(**res_json)

    def create(self, name, as_json=False):
        """Create new group.

        https://developers.mailerlite.com/v2/reference#create-group

        Parameters
        ----------
        name : str
            group name
        as_json : bool
            return result as json format
        Returns
        -------
        group: :class:Group
            group object
        """
        url = client.build_url('groups')
        data = {'name': name}
        res_code, res_json = client.post(url, body=data, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Group(**res_json)

    def add_subscribers(self, group_id, subscribers_data, resubscribe=False,
                        autoresponders=False, as_json=False):
        """Add one or many new subscribers to specified group at once.

        https://developers.mailerlite.com/v2/reference#add-single-subscriber
        https://developers.mailerlite.com/v2/reference#add-many-subscribers

        Parameters
        ----------
        group_id : int
            group id
        subscribers_data : dict, list of dict
            subscribers element that contains email and name
        resubscribe : bool
            reactivate subscriber if value is true (default False)
        autoresponders : bool
            autoresponders will be sent if value is true (default False)
        as_json : bool
            return result as json format
        Returns
        -------
        group: :class:Group
            group object
        """
        url = client.build_url('groups', group_id, 'subscribers', 'import')

        body = {'resubscribe': resubscribe, 'autoresponders': autoresponders}
        if isinstance(subscribers_data, dict):
            body['subscribers'] = list(subscribers_data)
        elif isinstance(subscribers_data, list):
            body['subscribers'] = subscribers_data
        else:
            raise ValueError('subscribers_data should be a dict or a list of'
                             ' dict that contains the following keys: email,'
                             ' name')

        errors = [d for d in body['subscribers'] if 'email' not in d.keys()
                  if 'name' not in d.keys()]
        if errors:
            raise ValueError('All subscribers_data should contain the'
                             ' following keys: email, name')
        res_code, res_json = client.post(url, body=body, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Subscriber(**res_json)

    def subscribers(self, group_id, limit=100, offset=0, stype=None,
                    as_json=False):
        """Get all subscribers in a specified group.

        https://developers.mailerlite.com/v2/reference#subscribers-in-a-group

        Parameters
        ----------
        group_id : int
            group id
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

        url = client.build_url('groups', group_id, 'subscribers', **params)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        for res in res_json:
            res['fields'] = [Field(**field) for field in res['fields']]

        all_subscribers = [Subscriber(**res) for res in res_json]
        return all_subscribers

    def subscriber(self, group_id, subscriber_id, as_json=False):
        """Get one subscriber in a specified group.

        https://developers.mailerlite.com/v2/reference#a-subscriber-of-a-group

        Parameters
        ----------
        group_id : int
            group id
        subscriber_id : int
            subscriber id
        as_json : bool
            return result as json format
        Returns
        -------
        subscriber: :class:Subscriber
            a single subscriber
        """
        url = client.build_url('groups', group_id, 'subscribers',
                               subscriber_id)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        res_json['fields'] = [Field(**res) for res in res_json['fields']]

        return Subscriber(**res_json)

    def delete_subscriber(self, group_id, subscriber_id):
        """Remove a subscribers.

        Parameters
        ----------
        group_id : int
            group id
        subscriber_id : int
            subscriber id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('groups', group_id, 'subscribers',
                               subscriber_id)
        return client.delete(url, headers=self.headers)
