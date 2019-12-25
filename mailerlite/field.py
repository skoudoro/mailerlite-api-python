"""Manage Fields."""

import mailerlite.client as client
from mailerlite.constants import Field


class Fields:

    def __init__(self, headers):
        """Initialize Fields object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def all(self, as_json=False):
        """Get list of fields from your account.

        https://developers.mailerlite.com/v2/reference#all-fields

        Parameters
        ----------
        as_json : bool
            return result as json format

        Returns
        -------
        fields: list
            all desired Fields.
        """
        url = client.build_url('fields')
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        all_fields = [Fields(**res) for res in res_json]
        return all_fields

    def get(self, id, as_json=False):
        """Get single field by ID from your account.

        look at https://developers.mailerlite.com/v2/reference#all-fields

        Parameters
        ----------
        id : int
            should be group id. e.g: id=1343965485
        as_json : bool
            return result as json format
        Returns
        -------
        Field: :class:Field
            a single field
        """
        url = client.build_url('fields', id)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Field(**res_json)

    def delete(self, id):
        """Remove custom field from account.

        https://developers.mailerlite.com/v2/reference#remove-field

        Parameters
        ----------
        id : int
            field id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('fields', id)
        return client.delete(url, headers=self.headers)


    # def update(self):
    #     pass

    # def create(self):
    #     pass
