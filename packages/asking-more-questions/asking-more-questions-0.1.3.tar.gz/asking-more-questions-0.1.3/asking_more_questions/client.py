import typer
import tabulate
import enum

from typing import Optional, List

from . models import Connection
from . models import DSN

from . connections import connection_list
from . connections import connection_delete
from . connections import connection_save
from . connections import connection_get


app = typer.Typer()


@app.command()
def connection(name: Optional[str] = typer.Argument(None), delete: Optional[bool] = None):
    ''' List or configure the API connections '''
    if not name:
        print_connection_list()
        return

    if delete:
        confirmation = typer.confirm(f'Really delete {name}?')
        if confirmation:
            connection_delete(name)
            typer.echo(f'Connection {name} is deleted!')
            return

    try:
        connection = connection_get(name)
        typer.echo('Updating existing connection')

    except ValueError:
        typer.echo('Setting up new connection')
        connection = None

    if not connection:
        connection = Connection(
            name=name,
            dsn=typer.prompt('Choose DSN', type=DSN, show_choices=True).value,
            usr=typer.prompt('Enter user'),
            pwd=typer.prompt(
                'Enter password',
                hide_input=True
            )
        )

    else:
        connection = Connection(
            name=name,
            dsn=typer.prompt('Enter DSN', default=connection.dsn, type=DSN, show_default=True, show_choices=True).value,
            usr=typer.prompt('Enter user', default=connection.usr),
            pwd=typer.prompt(
                'Enter password',
                default=connection.pwd,
                hide_input=True,
                show_default=False
            )
        )

    connection_save(*connection)
    typer.echo(f'Saved {name}!')


def print_connection_list():
    print(
        tabulate.tabulate(
            [
                {
                    key: val for (key, val) in connection.__dict__.items()
                    if key != 'pwd'
                }
                for connection
                in connection_list()
            ],
            headers='keys'
        )
    )

if __name__ == '__main__':
    app()