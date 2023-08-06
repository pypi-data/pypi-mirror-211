"""@Author: Rayane AMROUCHE

Utils for sources.
"""

from typing import Optional, Tuple
from dotenv import dotenv_values

from datachain.config import Params


def login(
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_env: str = "",
    password_env: str = "",
) -> Tuple[str, str]:
    """Login function to retrieve username and password.

    Args:
        username (Optional[str], optional): The username. Defaults to None.
        password (Optional[str], optional): The password. Defaults to None.
        username_env (str, optional): The environment variable name for the username.
        Defaults to "".
        password_env (str, optional): The environment variable name for the password.
        Defaults to "".

    Raises:
        AttributeError: Raised when neither the username nor the name of the username in
        the environment was given.
        AttributeError: Raised when neither the password nor the name of the password in
        the environment was given.

    Returns:
        Tuple[str, str]: A tuple containing the username and password.
    """
    try:
        if not username:
            username = dotenv_values(Params.env_path)[username_env]
    except KeyError as _:
        raise AttributeError(
            "Neither the username nor a valid username in the environment was given."
        ) from _

    try:
        if not password:
            password = dotenv_values(Params.env_path)[password_env]
    except KeyError as _:
        raise AttributeError(
            "Neither the password nor a valid password in the environment was given."
        ) from _

    return username, password
