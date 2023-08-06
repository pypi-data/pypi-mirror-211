"""@Author: Rayane AMROUCHE

Http source.
"""

from typing import Any

from datachain import DataSource


from datachain_sources.files._pandas import read_pandas


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(read_pandas, **kwds)

    schema = {
        "path": "http_uri",
        "request_type": "get | post",
        "data": "optional_argument",
        "json": "optional_argument",
        "params": "optional_argument",
        "headers": "optional_argument",
        "cookies": "optional_argument",
        "files": "optional_argument",
        "auth": "optional_argument",
        "timeout": "optional_argument",
        "allow_redirects": "optional_argument",
        "proxies": "optional_argument",
        "hooks": "optional_argument",
        "stream": "optional_argument",
        "verify": "optional_argument",
        "cert": "optional_argument",
    }
