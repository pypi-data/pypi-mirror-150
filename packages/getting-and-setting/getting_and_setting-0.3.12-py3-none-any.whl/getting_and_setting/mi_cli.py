import typer
import tabulate
import enum

from typing import Optional, List
from pathlib import Path

from . mi_api import MiApi
from . mi_endpoints import mi_endpoint_get

from . mi_endpoints import mi_endpoint_delete
from . mi_endpoints import mi_endpoint_get
from . mi_endpoints import mi_endpoint_list
from . mi_endpoints import mi_endpoint_save

from . mi_outputs import mi_output_generate_template
from . mi_models import Endpoint


Keys = enum.Enum(
    'Keys',
    {
        field: field
        for field
        in Endpoint.__dataclass_fields__.keys()
    }
)

Names = enum.Enum(
    'Names',
    {
        endpoint.name: endpoint.name
        for endpoint
        in mi_endpoint_list()
    }
)

app = typer.Typer()


@app.command()
def execute(endpoint: str, program: str, transaction: str, params: Optional[List[str]] = typer.Argument(None)):
    '''Excecute API calls and print the results '''
    try:
        params =  {
            f'{row.split("=")[0]}': row.split('=')[1]
            for row in params
        }
    except:
        typer.echo(f'Failed to parse extra parameters!\n {params}\n Has to have format KEY=VALUE')
        return
    
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.execute(program, transaction, **params)

    print('\n')
    print(
        tabulate.tabulate(
            [
                record for record
                in records.records
            ], headers='keys'
        )
    )


@app.command()
def meta(endpoint: Names, program: Optional[str] = typer.Argument(None), transaction: Optional[str] = typer.Argument(None)):
    ''' Show metadata by listing programs, program transaction and transaction details'''

    if not program and not transaction:
        print_program_list(endpoint.name)

    elif program and not transaction:
        print_program_meta(endpoint.name, program)

    elif program and transaction:
        print_transaction_meta(endpoint.name, program, transaction)


@app.command()
def template(endpoint_name: Names, program: str, transaction: str, path: Optional[Path] = typer.Argument(None)):
    '''Generate template file for SmartDataTool'''
    if not path:
        path = Path("~/")
    elif not path.absolute().is_dir():
        print("Enter a path only")
        return

    endpoint = mi_endpoint_get(endpoint_name.value)
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    mi_output_generate_template(
        api.transaction_meta(
            program,
            transaction
        ),
        path.absolute()
    )

@app.command()
def endpoint(name: Optional[str] = typer.Argument(None), delete: Optional[bool] = None):
    ''' List or configure the API endpoints '''
    if not name:
        print_endpoint_list()
        return

    if delete:
        confirmation = typer.confirm(f'Really delete {name}?')
        if confirmation:
            mi_endpoint_delete(name)
            typer.echo(f'Endpoint {name} is deleted!')
            return

    try:
        endpoint = mi_endpoint_get(name)
        typer.echo('Updating existing endpoint')

    except ValueError:
        typer.echo('Setting up new endpoint')
        endpoint = None

    if not endpoint:
        endpoint = Endpoint(
            name=name,
            host=typer.prompt('Enter host'),
            port=typer.prompt('Enter port'),
            usr=typer.prompt('Enter user'),
            pwd=typer.prompt(
                'Enter password',
                hide_input=True
            )
        )

    else:
        endpoint = Endpoint(
            name=name,
            host=typer.prompt('Enter host', default=endpoint.host),
            port=typer.prompt('Enter port', default=endpoint.port),
            usr=typer.prompt('Enter user', default=endpoint.usr),
            pwd=typer.prompt(
                'Enter password',
                default=endpoint.pwd,
                hide_input=True,
                show_default=False
            )
        )

    mi_endpoint_save(endpoint)
    typer.echo(f'Saved {name}!')


def print_transaction_meta(endpoint: str, program: str, transaction: str):
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.transaction_meta(program, transaction)

    typer.echo(f'{records.program}/{records.transaction}')
    typer.echo('\nInputs:')
    print(
        tabulate.tabulate(
            [
                input.__dict__ for input in
                records.inputs
            ],
            headers='keys'
        )
    )   

    typer.echo('\nOutputs:')
    print(
        tabulate.tabulate(
            [
                output.__dict__ for output in
                records.outputs
            ],
            headers='keys'
        )
    )


def print_program_meta(name: str, program: str):
    endpoint = mi_endpoint_get(name)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.program_meta(program)

    typer.echo(f'{records.program} - {records.description}\n')
    
    print(
        tabulate.tabulate(
            [
                {
                    'transaction': transaction.transaction,
                    'description': transaction.description
                }
                for transaction in
                records.transactions
            ],
            headers='keys'
        )
    )


def print_program_list(name: str):
    endpoint = mi_endpoint_get(name)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.program_list()

    for row in records.records:
        typer.echo(row)


def print_endpoint_list():
    print(
        tabulate.tabulate(
            [
                {
                    key: val for (key, val) in endpoint.__dict__.items()
                    if key != 'pwd'
                }
                for endpoint
                in mi_endpoint_list()
            ],
            headers='keys'
        )
    )

if __name__ == '__main__':
    app()