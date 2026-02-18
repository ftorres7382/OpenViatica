'''
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword  
'''

import typer
from ._core import ovutils

app = typer.Typer(
    help="ovutils is a python based data analytics workspace creation and management engine",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
    )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()

@app.command()
def fibonacci(n: int) -> None:
    result = ovutils.fibonacci(n)
    print(result)
    
@app.command()
def fibonacci_rust(n: int) -> None:
    result = ovutils.fibonacci_rust(n)
    print(result)

if __name__ == "__main__":
    app()