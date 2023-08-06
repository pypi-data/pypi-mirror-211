"""@Author: Rayane AMROUCHE

File source.
"""

from typing import Any
from datachain_sources.files._ftp import ftp_to_file
from datachain_sources.files._local import local_to_file

try:
    from datachain_sources.files._sftp import sftp_to_file
except ImportError:
    sftp_to_file = None

try:
    from datachain_sources.files._http import http_to_file
except ImportError:
    http_to_file = None


def get_file(path: str, *args: Any, **kwds: Any) -> bytes:
    """Reads bytes from a path or file server URL.

    Args:
        path (str): The path or file URL to the file to read.

    Returns:
        bytes: The bytes read from the file.
    """
    if path.startswith(("http://", "https://")):
        if http_to_file is None:
            raise ImportError(
                "Module 'requests' is missing. "
                "It is needed to execute HTTP requests."
            )
        return http_to_file(path, *args, **kwds)
    if path.startswith("ftp://"):
        return ftp_to_file(path)
    if path.startswith("sftp://"):
        if sftp_to_file is None:
            raise ImportError(
                "Module 'paramiko' is missing. "
                "It is needed to execute SFTP requests."
            )
        return sftp_to_file(path)
    return local_to_file(path)
