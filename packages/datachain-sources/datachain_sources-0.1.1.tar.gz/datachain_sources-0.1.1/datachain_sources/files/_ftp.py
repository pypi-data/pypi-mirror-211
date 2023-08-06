"""@Author: Rayane AMROUCHE

Ftp source.
"""

import io
import ftplib


def ftp_to_file(ftp_url: str) -> bytes:
    """Retrieves bytes from an FTP path.

    Args:
        ftp_url (str): The URL of the FTP server.

    Returns:
        io.BytesIO: A file-like object containing the bytes read from the FTP path.

    Raises:
        ftplib.all_errors: If an error occurs while accessing the FTP server.
    """
    # Split the FTP URL into its components
    parts = ftp_url.split("/")
    username_password = parts[2].split("@")[0]
    username, password = username_password.split(":")
    server = parts[2].split("@")[1]
    path = "/" + "/".join(parts[3:])

    # Connect to the FTP server and retrieve the file
    with ftplib.FTP(server) as ftp:
        ftp.login(user=username, passwd=password)
        with ftp.retrbinary(f"RETR {path}", callback=None) as file:
            data_bytes = file.read()
            data = io.BytesIO(data_bytes)
            return data
