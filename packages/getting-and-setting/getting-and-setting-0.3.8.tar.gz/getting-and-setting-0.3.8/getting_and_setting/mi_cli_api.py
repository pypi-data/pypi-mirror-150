import typer

from typing import List
from typing import Optional

import tabulate

from . import MiApi

from . mi_endpoints import mi_endpoint_get

from . mi_models import MiRecords
from . mi_models import MiError

app = typer.Typer(help='Interact with the API')

@app.command()
def execute(endpoint: str, program: str, transaction: str, params: Optional[List[str]] = typer.Argument(None)):
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
