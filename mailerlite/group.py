"""Manage Groups."""

import mailerlite.client as client
from mailerlite.constants import Subscriber, Group


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
        url = client.build_url('subscribers')
        data = {'name': name}
        res_code, res_json = client.post(url, body=data, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Group(**res_json)
