
import pyodbc as odbc
import enum
from dataclasses import dataclass
from dataclasses import asdict

DSN = enum.Enum(
    'DSN',
    {
        key: key for key
        in odbc.dataSources().keys()
    }
)

@dataclass
class Base:
    def __iter__(self):
        return iter(asdict(self).values())

@dataclass
class Connection(Base):
    name: str
    dsn: str
    usr: str
    pwd: str
