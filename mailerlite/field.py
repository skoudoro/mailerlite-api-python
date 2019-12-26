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

    def delete(self, field_id):
        """Remove custom field from account.

        https://developers.mailerlite.com/v2/reference#remove-field

        Parameters
        ----------
        field_id : int
            field id

        Returns
        -------
        success: bool
            deletion status
        """
        url = client.build_url('fields', field_id)
        return client.delete(url, headers=self.headers)

    def update(self, field_id, title, as_json=False):
        """Update custom field in account.

        https://developers.mailerlite.com/v2/reference#update-field

        Parameters
        ----------
        field_id : int
            field id
        title : str
            Title of field

        Returns
        -------
        field : :class:Field
            field object updated
        """
        url = client.build_url('fields', field_id)
        body = {"title": title}
        res_code, res_json = client.put(url, body=body, headers=self.headers)

        if as_json or not res_json:
            return res_json

        return Field(**res_json)

    def create(self, title, field_type='TEXT'):
        """Create new custom field in account.

        https://developers.mailerlite.com/v2/reference#create-field

        Parameters
        ----------
        title : str
            Title of field
        field_type: str
            Type of field. Available values: TEXT , NUMBER, DATE
            (default: TEXT)

        Returns
        -------
        field : :class:Field
            field object updated
        """
        if field_type.upper() not in ['TEXT', 'NUMBER', 'DATE']:
            raise ValueError('Incorrect field_type. Available values'
                             ' are: TEXT , NUMBER, DATE')
        url = client.build_url('fields')
        data = {'title': title, 'type': field_type.upper()}
        return client.post(url, body=data, headers=self.headers)
