import pyodbc as odbc
import pandas as pd

from typing import Union
from . connections import Names
from . connections import connection_get

def query(sql: str, name: Union[Names, str]) -> pd.DataFrame:
    name = name.value if isinstance(name, Names) else name 
    connection = connection_get(name)

    with odbc.connect(**connection) as conn:
        return pd.read_sql(sql, conn)
