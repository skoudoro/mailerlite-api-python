"""Manage Segments."""

import mailerlite.client as client
from mailerlite.constants import Segment, Meta, Pagination


class Segments:

    def __init__(self, headers):
        """Initialize Segments object.

        Parameters
        ----------
        headers : dict
            request header containing your mailerlite api_key.
            More information : https://developers.mailerlite.com/docs/request
        """
        if not headers:
            raise ValueError("Empty headers. Please enter a valid one")

        self.headers = headers

    def all(self, limit=100, offset=0, order='asc', as_json=False):
        """Get paginated details of all segments from your account.

        look at https://developers.mailerlite.com/reference#segments-1

        Parameters
        ----------
        limit : int
            How many segments you want
        offset : int
            page index
        order : str
            pick the order. Here are the possible values: ASC (default) or DESC
        as_json : bool
            return result as json format

        Returns
        -------
        segments: list
            all desired segment. More informations:
            https://developers.mailerlite.com/v2/reference#segments-1
        meta: object
            some meta informations about the segments
        """
        if order.upper() not in ['ASC', 'DESC']:
            raise IOError("Incorrect order, please choose between ASC or DESC")

        params = {'limit': limit, 'offset': offset, 'order': order}
        url = client.build_url('segments', **params)
        res_code, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json['data'], res_json['meta']

        all_segments = [Segment(**res) for res in res_json['data']]
        res_json['meta']['pagination'] = Pagination(**res_json['meta']
                                                    .pop('pagination'))
        meta = Meta(**res_json['meta'])
        return all_segments, meta

    @property
    def count(self):
        """Return the number of segments.

        look at https://developers.mailerlite.com/reference#section-segmentscount

        Returns
        -------
        count: int
            number of segments
        """
        url = client.build_url('segments', 'count')
        res_code, res_json = client.get(url, headers=self.headers)
        return res_json['count']
