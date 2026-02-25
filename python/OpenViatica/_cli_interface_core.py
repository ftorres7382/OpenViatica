'''
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword  
'''

import typer
from ._core import ovutils

app = typer.Typer(
    help="'ovutils' is a python based data analytics workspace creation and management engine",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
    )
# Creating an alias for better organization
ovutils_app = app

ovutils_ws_app = typer.Typer(
    help="'ovutils ws' is a workspace creation and management CLI tool."
    )

ovutils_app.add_typer(ovutils_ws_app, name="ws")

# Routiung
@ovutils_ws_app.command("init")
def ovutils_ws_init() -> None:
    '''Initializes a new workspace'''
    ovutils.ws.init()



# Default callbacks for whenever the tool is called without any arguments
@ovutils_app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()

@ovutils_ws_app.callback(invoke_without_command=True)
def ws_main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()

if __name__ == "__main__":
    app()