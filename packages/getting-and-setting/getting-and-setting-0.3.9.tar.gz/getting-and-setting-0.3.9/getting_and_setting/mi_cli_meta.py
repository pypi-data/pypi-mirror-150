import typer
import tabulate

from typing import List
from typing import Optional

from . import MiApi
from . mi_endpoints import mi_endpoint_get

app = typer.Typer(help='Fetch metadata')

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


def print_program_meta(endpoint: str, program: str):
    endpoint = mi_endpoint_get(endpoint)
    
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


def print_program_list(endpoint: str):
    endpoint = mi_endpoint_get(endpoint)
    
    api = MiApi(endpoint.host, endpoint.port, endpoint.usr, endpoint.pwd)
    records = api.program_list()

    for row in records.records:
        typer.echo(row)


@app.command()
def show(endpoint: str, program: Optional[str] = typer.Argument(None), transaction: Optional[str] = typer.Argument(None)):
    if not program and not transaction:
        print_program_list(endpoint)

    elif program and not transaction:
        print_program_meta(endpoint, program)

    elif program and transaction:
        print_transaction_meta(endpoint, program, transaction)
        


