'''
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword  
'''
# TODO:

# README.md not intuitive enough, find another filename that screams click and read me please
    # SECTION_PURPOSE.md
    # HOW_TO_GET_STARTED.md
# Make the purpose of the Docs folder more apparent
# Home
# make purpose of each folder more clear, especially repos
import typer
from OpenViatica import ovutils

app = typer.Typer(
    help="OpenVitaca Utilities ('ovutils'): A workspace creation and management engine\n\nGETTING STARTED:\nRun the command inside the quotes: 'ovutils ws init'",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
    )
# Creating an alias for better organization
ovutils_app = app

# Create the ws app and add to the set of commands that can be done
ovutils_ws_app = typer.Typer(
    help="For creating and managing independent OpenViatica workspaces."
    )
ovutils_app.add_typer(ovutils_ws_app, name="ws")

# Create the ws sub apps
ovutils_ws_meta_app = typer.Typer(
    help="For creating and managing a workspace that manages other workspaces."
    )
ovutils_ws_app.add_typer(ovutils_ws_meta_app, name="meta-ws")

# ovutils Routing
@ovutils_app.command("init")
def ovutils_init() -> None:
    '''Initializes a new OpenViatica workspace'''
    print("Hello")


# ws Routing
@ovutils_ws_meta_app.command("init")
def ovutils_ws_init() -> None:
    '''Initializes a new OpenViatica Meta workspace'''
    meta_ws = ovutils.MetaWorkspace()
    meta_ws.initialize()



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

@ovutils_ws_meta_app.callback(invoke_without_command=True)
def ws_meta_main(ctx: typer.Context) -> None:
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