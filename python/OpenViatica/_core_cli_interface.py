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
from OpenViatica._types import ov_ws_type_t
import typing as t

# Entry point for the application
app = typer.Typer(
    help="OpenVitaca Utilities ('ovutils'): A workspace creation and management engine\n\nGETTING STARTED:\nRun the command inside the quotes: 'ovutils ws init'",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
    )
# Creating an alias for better organization
ovutils_app = app

# Create the ws app and add to the set of commands that can be done
ovutils_wsTools_app = typer.Typer(
    help="Tools for creating and managing individual OpenViatica workspaces.",
    name="ws-tools"
    )
ovutils_app.add_typer(ovutils_wsTools_app)

# Create the ws sub apps
## ov-meta
ovutils_wsTools_ovMeta_app = typer.Typer(
    help="OpenViatica Meta Workspace: For creating and managing a workspace that links other workspaces.",
    name="ov-meta"
    )
ovutils_wsTools_app.add_typer(ovutils_wsTools_ovMeta_app)

## ov-templates
ovutils_wsTools_ovTemplates_app = typer.Typer(
    help="OpenViatica Templates Workspace: For creating and managing template files and folders.",
    name="ov-templates"
    )
ovutils_wsTools_app.add_typer(ovutils_wsTools_ovTemplates_app)


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
## ov-meta
@ovutils_wsTools_ovMeta_app.command("init")
def ovutils_wstools_meta_init(
    # Initialize function args
    ws_id: str | None = None,
    ws_name: str | None = None,

    # Class init args
    ws_path:str = "./",
    workspace_metadata_path:str | None = None,
    workspace_toml_filename: str | None = None,
    
    # Other args
    debug:bool = False
) -> None:
    '''Initializes a new OpenViatica Meta workspace'''

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
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

@ovutils_wsTools_ovMeta_app.command("link")
def ovutils_wstools_meta_link(
    # Function args
    target_ws_path:str,
    target_ws_type:ov_ws_type_t,
    target_workspace_metadata_path:str | None = None,
    target_workspace_toml_filename: str | None = None,

    # Class init args
    subject_ws_path:str = "./",
    subject_workspace_metadata_path:str | None = None,
    subject_workspace_toml_filename: str | None = None,

    
    # Other args
    debug:bool = False
) -> None:
    '''Links a OpenViatica workspace to a Meta workspace'''

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=subject_ws_path,
            _workspace_metadata_path = subject_workspace_metadata_path,
            _workspace_toml_filename = subject_workspace_toml_filename
        )
        meta_ws.link(
            target_workspace_path=target_ws_path,
            target_workspace_type=target_ws_type,
            _target_workspace_metadata_path = target_workspace_metadata_path,
            _target_workspace_toml_filename = target_workspace_toml_filename
        )

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass

@ovutils_wsTools_ovMeta_app.command("unlink")
def ovutils_wstools_meta_unlink(
    # Function args
    target_ws_path:str,
    target_ws_type:ov_ws_type_t,
    target_workspace_metadata_path:str | None = None,
    target_workspace_toml_filename: str | None = None,

    # Class init args
    subject_ws_path:str = "./",
    subject_workspace_metadata_path:str | None = None,
    subject_workspace_toml_filename: str | None = None,

    
    # Other args
    debug:bool = False
) -> None:
    '''Links a OpenViatica workspace to a Meta workspace'''

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=subject_ws_path,
            _workspace_metadata_path = subject_workspace_metadata_path,
            _workspace_toml_filename = subject_workspace_toml_filename
        )
        meta_ws.unlink(
            target_workspace_path=target_ws_path,
            target_workspace_type=target_ws_type,
            _target_workspace_metadata_path = target_workspace_metadata_path,
            _target_workspace_toml_filename = target_workspace_toml_filename
        )

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass   

@ovutils_wsTools_ovMeta_app.command("exec",context_settings={
    "allow_extra_args": True, 
    "ignore_unknown_options": True
})
def ovutils_wstools_meta_exec(
    ctx: typer.Context,
    identifier: str,
    identifier_type: t.Literal["id", "name"],

    # Class init args
    ws_path:str = "./",
    workspace_metadata_path:str | None = None,
    workspace_toml_filename: str | None = None,

    
    # Other args
    debug:bool = False
) -> None:
    '''Executes a command to a linked OpenViatica workspace'''

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path = workspace_metadata_path,
            _workspace_toml_filename = workspace_toml_filename
        )

        # Get the workspace object to validate the access
        workspace_object = meta_ws.get_linked_workspace_object(
            identifier=identifier,
            identifier_type=identifier_type,
        )

        # Add the base workspace context information to the arguments if the areguments are nor blank at the moment
        if not isinstance(ovutils_wsTools_app.info.name, str):
                raise TypeError("ovutils_wsTools_app.info.name is NOT string!")
        set_args: t.List[str] = [
            # Extract the command str from the app itself
            ovutils_wsTools_app.info.name,

            # Add at least the workspace endpoint to start with
            workspace_object.WORKSPACE_TYPE
        ]
        
        # If the original arguments were help arguments, then add the help arg
        only_help_args = False
        if len(ctx.args) == 1 and ("-h" in ctx.args or "--help" in ctx.args):
            set_args += ctx.args
            only_help_args = True
        
        # If the original arguments were both ways of asking for help, pass them on too
        if len(ctx.args) == 2 and "-h" in ctx.args and "--help" in ctx.args:
            set_args += ctx.args
            only_help_args = True
            
        
        # If there were other arguments already in there (that are not ONLY help arguments), then inject extra ones to make the commands cwd agnostic
        if len(ctx.args) > 0 and not only_help_args:
            # Split the first argument which is the function to be run, inject the base context, add the rest
            set_args += [ctx.args[0]] +[
                "--ws-path", workspace_object.workspace_path,
                "--workspace-metadata-path", workspace_object.workspace_metadata_path,
                "--workspace-toml-filename", workspace_object.workspace_toml_filename
            ] + ctx.args[1:]
        ctx.args = set_args            


        # Allow piping the command to the other app
        ovutils_app(args=ctx.args, standalone_mode=False)

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass   


## ov-templates  
@ovutils_wsTools_ovTemplates_app.command("init")   
def ovutils_wstools_templates_init(
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
    '''Initializes a new OpenViatica Templates workspace'''

    def run() -> None:
        templates_ws = ovutils.WorkspaceTools.TemplatesWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path = workspace_metadata_path,
            _workspace_toml_filename = workspace_toml_filename
        )
        templates_ws.initialize(
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

@ovutils_wsTools_app.callback(invoke_without_command=True)
def ovutils_wstools_main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()

@ovutils_wsTools_ovMeta_app.callback(invoke_without_command=True)
def ovutils_wstools_meta_main(ctx: typer.Context) -> None:
    """
    OpenViatica Utilities CLI.
    """
    if ctx.invoked_subcommand is None:
        # This prints the help menu to the console
        typer.echo(ctx.get_help())
        # This exits the program gracefully
        raise typer.Exit()



@ovutils_wsTools_ovTemplates_app.callback(invoke_without_command=True)
def ovutils_wstools_templates_main(ctx: typer.Context) -> None:
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