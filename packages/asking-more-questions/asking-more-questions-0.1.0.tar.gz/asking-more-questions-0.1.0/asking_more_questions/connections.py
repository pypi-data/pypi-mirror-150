import configparser
import keyring
import pathlib
import enum
from typing import Dict, List, Union

from . models import Connection

SERVICE_ID = 'asking-more-questions'
SERVICE_PATH = str(pathlib.Path.joinpath(pathlib.Path.home(), f'{SERVICE_ID}.ini').absolute())


def connection_save(name: str, dsn: str, usr: str, pwd: str) -> Connection:
    config = configparser.ConfigParser()
    config.read(SERVICE_PATH)

    config[f'connection.{name}'] = {
        'dsn': dsn,
        'usr': usr,
    }

    with open(SERVICE_PATH, 'w') as f:
        config.write(f)

    keyring.set_password(SERVICE_ID, name, pwd)

    return connection_get(name)


def connection_get(name: str) -> Connection:
    config = configparser.ConfigParser()
    config.read(SERVICE_PATH)

    try:
        connection = dict(config[f'connection.{name}'])

    except KeyError:
        raise ValueError(f'Connection {name} not found in configuration')

    connection['pwd'] = keyring.get_password(SERVICE_ID, name)

    return Connection(name=name, **connection)


def connection_delete(name: str) -> None:
    config = configparser.ConfigParser()
    config.read(SERVICE_PATH)

    config.remove_section(f'connection.{name}')

    with open(SERVICE_PATH, 'w') as f:
        config.write(f)

    try:
        keyring.delete_password(SERVICE_ID, name)

    except keyring.core.backend.errors.PasswordDeleteError:
        pass


def connection_list() -> List[Connection]:
    config = configparser.ConfigParser()
    config.read(SERVICE_PATH)

    return [
        Connection(
            name = config[section].name.split('.')[1],
            dsn = config[section]['dsn'],
            usr = config[section]['usr'],
            pwd = keyring.get_password(
                SERVICE_ID,
                config[section].name.split('.')[1]
            )
        )
        for section
        in config.sections()
        if section.startswith('connection')
    ]


Keys = enum.Enum(
    'Keys',
    {
        field: field
        for field
        in Connection.__dataclass_fields__.keys()
    }
)

Names = enum.Enum(
    'Names',
    {
        connection.name: connection.name
        for connection
        in connection_list()
    }
)