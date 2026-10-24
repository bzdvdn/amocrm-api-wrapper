from .legacy_client import AmoLegacyClient as AmoLegacyClient
from .oauth_client import AmoOAuthClient as AmoOAuthClient

__all__ = [
    "AmoLegacyClient",
    "AmoOAuthClient",
    "__version__",
]

__version__ = "1.0.1"
__author__ = "bzdvdn"
