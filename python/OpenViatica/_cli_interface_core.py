'''
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword  
'''
# TODO:
# Ask user to install directly or create a new folder
    # Option to turn this off
# Folder names default should be ov-workspace-##
    # Option to add id to folder
# README.md not intuitive enough, find another filename that screams click and read me please
    # SECTION_PURPOSE.md
    # HOW_TO_GET_STARTED.md
# Make the purpose of the Docs folder more apparent
# Home
# make purpose of each folder more clear, especially repos
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
    help="'ovutils ws' is a CLI tool for workspace creation and management."
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