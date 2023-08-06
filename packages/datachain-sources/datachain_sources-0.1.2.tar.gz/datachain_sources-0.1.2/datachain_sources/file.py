"""@Author: Rayane AMROUCHE

File source.
"""

from typing import Any

from datachain import DataSource

from datachain_sources.files._pandas import read_pandas, write_pandas


class TabularSource(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to read dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(read_pandas, **kwds)

    schema = {"path": "file_path"}


class TabularSink(DataSource):  # pylint: disable=too-few-public-methods
    """Pandas implementation of DataSource being able to write dataframes"""

    def __init__(self, **kwds: Any) -> None:
        super().__init__(write_pandas, **kwds)

    schema = {"path": "file_path"}
