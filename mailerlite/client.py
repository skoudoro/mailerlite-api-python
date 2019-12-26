"""Utility function for calling the API."""

from os.path import join as pjoin
import requests
from urllib.parse import urlencode
from mailerlite.constants import MAILERLITE_API_V2_URL, VALID_REQUEST_METHODS


def build_url(*path, **queryparams):
    """Build path with endpoint and args.

    Parameters
    ----------
    path : endpoint url
    queryparams : dict

    Returns
    -------
    url : str
      desired path
    """
    url = '/'.join(map(str, path))
    if queryparams:
        url += '?{}'.format(urlencode(queryparams))
    return url


def make_request(url, method, headers=None, data=None,
                 timeout=None, hooks=None):
    """Make the request to the API.

    Parameters
    ----------
    url : str
    method : str
    headers : dict, optional
        Dictionary of HTTP Headers to send
    data : dict, optional
        A JSON serializable Python object to send in the body
    timeout : int, optional
        How long to wait for the server to send data before giving up
    hooks : dict, optional

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API
    """
    if method not in VALID_REQUEST_METHODS:
        raise ValueError("Incorrect request method. method should be "
                         "{}".format(VALID_REQUEST_METHODS))

    url = pjoin(MAILERLITE_API_V2_URL, url)
    hooks = hooks or requests.hooks.default_hooks()
    headers = headers or requests.utils.default_headers()
    try:
        response = requests.request(**dict(method=method,
                                           url=url,
                                           json=data,
                                           timeout=timeout,
                                           hooks=hooks,
                                           headers=headers
                                           ))
    except requests.exceptions.RequestException as e:
        raise e
    else:
        if response.status_code >= 400:
            raise IOError(response)

        if response.status_code == 204:
            return None
        return response.status_code, response.json()

    return response.status_code, response.json()


def post(url, body=None, **kwargs):
    """Handle POST requests to add new information.

    Parameters
    ----------
    url : str
        The url for the endpoint including path parameters
    body : dict, optional
        The request body parameters. Default: None

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API

    """
    return make_request(url=url, method='POST', data=body, **kwargs)


def get(url, params=None, **kwargs):
    """Handle GET requests to obtain information.

    Parameters
    ----------
    url: str
        The url for the endpoint including path parameters
    params: dict, optional
        The query string parameters

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API
    """
    if params:
        url += '?' + urlencode(params)
    return make_request(url=url, method='GET', **kwargs)


def delete(url, **kwargs):
    """Handle DELETE requests to Remove information.

    Parameters
    ----------
    url: str
        The url for the endpoint including path parameters

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API
    """
    return make_request(url=url, method='DELETE', **kwargs)


def put(url, body=None, **kwargs):
    """Handle PUT requests to modify existing information.

    Parameters
    ----------
    url : str
        The url for the endpoint including path parameters
    body : dict, optional
        The request body parameters. Default: None

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API
    """
    return make_request(url=url, method='PUT', data=body, **kwargs)


def patch(url, body=None, **kwargs):
    """Handle PATCH requests.

    Parameters
    ----------
    url : str
        The url for the endpoint including path parameters
    body : dict, optional
        The request body parameters. Default: None

    Returns
    -------
    response : int
        response value
    content : dict
        The JSON output from the API
    """
    return make_request(url=url, method='PATCH', data=body, **kwargs)
