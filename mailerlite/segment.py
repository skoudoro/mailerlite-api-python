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
        valid_headers, error_msg = client.check_headers(headers)
        if not valid_headers:
            raise ValueError(error_msg)

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
        _, res_json = client.get(url, headers=self.headers)

        if as_json or not res_json:
            return res_json['data'], res_json['meta']

        all_segments = [Segment(**res) for res in res_json['data']]
        res_json['meta']['pagination'] = Pagination(**res_json['meta']
                                                    .pop('pagination'))
        meta = Meta(**res_json['meta'])
        return all_segments, meta

    def count(self):
        """Return the number of segments.

        More informations:
        https://developers.mailerlite.com/reference#section-segments-count

        Returns
        -------
        count: int
            number of segments

        """
        url = client.build_url('segments', 'count')
        _, res_json = client.get(url, headers=self.headers)

        return res_json.get('count') or len(res_json.get('data'))
