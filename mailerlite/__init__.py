from mailerlite.api import MailerLiteApi

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['MailerLiteApi', __version__]
