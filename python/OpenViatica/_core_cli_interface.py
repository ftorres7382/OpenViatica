'''
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword  
'''
# TODO:

# README.md not intuitive enough, find another filename that screams click and read me please
    # SECTION_PURPOSE.md
    # GETTING_STARTED.md
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
ovutils_wsTools_app = typer.Typer(
    help="Tools for creating and managing individual OpenViatica workspaces."
    )
ovutils_app.add_typer(ovutils_wsTools_app, name="ws-tools")

# Create the ws sub apps
ovutils_wsTools_ovMeta_app = typer.Typer(
    help="OpenViatica Meta Workspace: For creating and managing a workspace that manages other workspaces."
    )
ovutils_wsTools_app.add_typer(ovutils_wsTools_ovMeta_app, name="ov-meta")

# ovutils Routing
@ovutils_app.command("init")
def ovutils_init(
    # Class init args
    ws_path:str = "./",
    ws_metadata_path: None | str = None,   

    ## Meta workspace arguments, they get passed directly to the Meta workspace class
    meta_ws_path: str | None = None,
    meta_ws_metadata_path: str | None = None,
    meta_ws_toml_filename: str | None = None,

    # Initialize args
    ws_id: str | None = None,
    ws_name: str | None = None,

    # Other args
    debug:bool = False
) -> None:
    '''Initializes a new OpenViatica pre-configured workspace'''
    def run() -> None:
        ov_ws = ovutils(
            workspace_path=ws_path,
            _workspace_metadata_path = ws_metadata_path,
            
            _meta_workspace_path = meta_ws_path,
            _meta_workspace_metadata_path = meta_ws_metadata_path,
            _meta_workspace_toml_filename = meta_ws_toml_filename
        )
        ov_ws.initialize(
            workspace_id=ws_id,
            workspace_name=ws_name
        )

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass


# ws Routing
@ovutils_wsTools_ovMeta_app.command("init")
def ovutils_meta_ws_init(
    # Class init args
    ws_path:str = "./",
    workspace_metadata_path:str | None = None,
    workspace_toml_filename: str | None = None,
    
    # Initialize function args
    ws_id: str | None = None,
    ws_name: str | None = None,
    
    # Other args
    debug:bool = False
) -> None:
    '''Initializes a new OpenViatica Meta workspace'''

    def run() -> None:
        meta_ws = ovutils.WorkpaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path = workspace_metadata_path,
            _workspace_toml_filename = workspace_toml_filename
        )
        meta_ws.initialize(
            workspace_id=ws_id,
            workspace_name=ws_name
        )

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass
            

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

@ovutils_wsTools_ovMeta_app.callback(invoke_without_command=True)
def ws_meta_main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()

@ovutils_wsTools_app.callback(invoke_without_command=True)
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