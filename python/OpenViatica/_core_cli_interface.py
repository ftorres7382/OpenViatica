"""
The purpose of the _cli_interface is to map all the functions the user invokes through the CLI
to the appropriate user facing module and function.

The main function will be invokeable through the ovutils keyword
"""
# TODO:

# README.md not intuitive enough, find another filename that screams click and read me please
# SECTION_PURPOSE.md
# GETTING_STARTED.md
# Make the purpose of the Docs folder more apparent
# Home
# make purpose of each folder more clear, especially repos
import typer
from OpenViatica import ovutils


from OpenViatica._types import ov_ws_type_t, ov_ws_types
from OpenViatica._general_core import General as G
import typing as t

# Entry point for the application
app = typer.Typer(
    help="OpenVitaca Utilities ('ovutils'): A workspace creation and management engine\n\nGETTING STARTED:\nRun the command inside the quotes: 'ovutils ws init'",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)
# Creating an alias for better organization
ovutils_app = app


# Create the ws app and add to the set of commands that can be done
ovutils_wsTools_app = typer.Typer(
    help="Tools for creating and managing individual OpenViatica workspaces.",
    name="ws-tools",
)
ovutils_app.add_typer(ovutils_wsTools_app)


# Create the ws sub apps
## ov-meta
ovutils_wsTools_ovMeta_app = typer.Typer(
    help="OpenViatica Meta Workspace: For creating and managing a workspace that links other workspaces.",
    name="ov-meta",
)
ovutils_wsTools_app.add_typer(ovutils_wsTools_ovMeta_app)


## ov-templates
ovutils_wsTools_ovTemplates_app = typer.Typer(
    help="OpenViatica Templates Workspace: For creating and managing template files and folders.",
    name="ov-templates",
)
ovutils_wsTools_app.add_typer(ovutils_wsTools_ovTemplates_app)


# ovutils Routing
@ovutils_app.command("init")
def ovutils_init(
    # Class init args (Standardized in all functions for a reason)
    ws_path: t.Annotated[
        str, typer.Argument(help="The path to the workspace")
    ] = "./",  # positional arg for terminal
    ws_path_flag: t.Annotated[
        str | None, typer.Option("--ws-path", hidden=True)
    ] = None,
    ws_metadata_path: None | str = None,
    ## Meta workspace arguments, they get passed directly to the Meta workspace class
    meta_ws_path: str | None = None,
    meta_ws_metadata_path: str | None = None,
    meta_ws_toml_filename: str | None = None,
    # Initialize args
    ws_id: str | None = None,
    ws_name: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Initializes a new OpenViatica pre-configured workspace"""

    # Set a value for ws_path based on priority system
    if ws_path_flag is not None:
        ws_path = ws_path_flag

    def run() -> None:
        ov_ws = ovutils(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _meta_workspace_path=meta_ws_path,
            _meta_workspace_metadata_path=meta_ws_metadata_path,
            _meta_workspace_toml_filename=meta_ws_toml_filename,
        )

        workspace_toml_filepath = ov_ws.initialize(
            workspace_id=ws_id, workspace_name=ws_name
        )

        # Read in the workspace_toml to print info about the workspace
        workspace_dict = t.cast(
            ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            G.read_toml_dict(
                workspace_toml_filepath,
                expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            ),
        )
        # Since here we can assume we have a fully functioning workspace,
        #   then we can get the workspace object to print some stats for the workspace
        print(
            f"Successfully initialized an OpenViatica workspace called '{workspace_dict['name']}' in the folderpath '{ov_ws.workspace_path}'"
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
    # Class init args (Standardized in all functions for a reason)
    ws_path: t.Annotated[
        str, typer.Argument(help="The path to the workspace")
    ] = "./",  # positional arg for terminal
    ws_path_flag: t.Annotated[
        str | None, typer.Option("--ws-path", hidden=True)
    ] = None,
    ws_metadata_path: str | None = None,
    ws_toml_filename: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Initializes a new OpenViatica Meta workspace"""

    # Set a value for ws_path based on priority system
    if ws_path_flag is not None:
        ws_path = ws_path_flag

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _workspace_toml_filename=ws_toml_filename,
        )
        workspace_toml_filepath = meta_ws.initialize(
            workspace_id=ws_id, workspace_name=ws_name
        )

        # Read in the workspace_toml to print info about the workspace
        workspace_dict = t.cast(
            ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            G.read_toml_dict(
                workspace_toml_filepath,
                expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            ),
        )
        # Since here we can assume we have a fully functioning workspace,
        #   then we can get the workspace object to print some stats for the workspace
        print(
            f"Successfully initialized an OpenViatica Meta workspace called '{workspace_dict['name']}' in the folderpath '{meta_ws.workspace_path}'"
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
    target_or_subject_ws_path: str = typer.Argument(
        ...,
        help="- Target workspace path if only one path is provided.\n\
        - Subject workspace path if two workspace paths are provided.",
    ),
    target_ws_path: str | None = typer.Argument(None),
    target_ws_type: ov_ws_type_t | None = None,
    target_ws_metadata_path: str | None = None,
    target_workspace_toml_filename: str | None = None,
    # Class init args (Standardized in all functions for a reason)
    ws_path_flag: t.Annotated[
        str | None, typer.Option("--ws-path", hidden=True)
    ] = None,
    ws_metadata_path: str | None = None,
    ws_toml_filename: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Links a OpenViatica workspace to a Meta workspace"""
    ws_path_flag_is_user_defined = ws_path_flag is not None

    # Set a default value for the ws_path_flag
    if ws_path_flag is None:
        ws_path_flag = "./"

    # Set default value for ws_path value
    ws_path = ws_path_flag

    # Based on the definition in the annotations, we are garenteed that the first argument IS defined.
    # Check only the second argument

    if target_ws_path is None:
        # Scenario: User provided [TARGET] (subject defaults to flag/current dir)
        # If the second argument is not defined, then the first argument IS the target workspace path
        target_ws_path = target_or_subject_ws_path

    else:
        # Scenario: User provided [SUBJECT] [TARGET]
        # If the second argument has been defined, then the first one is the subject workspace path

        # If the workspace path flag was defined AND the workspace path was also defined by the user, raise an error
        if ws_path_flag_is_user_defined:
            raise ValueError(
                "Both 'ws_path_flag' and a positional 'ws-path' cannot be defined in the same command."
            )

        ws_path = target_or_subject_ws_path

    # After this line, by default the subject workspace path is
    #   the ws_path_flag if one positional arg was defined
    #   The subject workspace path is changed to positional arguments if both positional arguments were defined
    # Target workspace path is set implicitly for the single arg example, explicitly if two arguments were provided.
    # We are now garenteed a value for the subject and target workspace path after this line

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _workspace_toml_filename=ws_toml_filename,
        )
        meta_ws.link(
            target_workspace_path=target_ws_path,
            target_workspace_type=target_ws_type,
            _target_workspace_metadata_path=target_ws_metadata_path,
            _target_workspace_toml_filename=target_workspace_toml_filename,
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
    target_or_subject_ws_path: str = typer.Argument(
        ...,
        help="- Target workspace path if only one path is provided.\n\
        - Subject workspace path if two workspace paths are provided.",
    ),
    target_ws_path: str | None = typer.Argument(None),
    target_ws_type: ov_ws_type_t | None = None,
    target_ws_metadata_path: str | None = None,
    target_workspace_toml_filename: str | None = None,
    # Class init args (Standardized in all functions for a reason)
    ws_path_flag: t.Annotated[
        str | None, typer.Option("--ws-path", hidden=True)
    ] = None,
    ws_metadata_path: str | None = None,
    ws_toml_filename: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Links a OpenViatica workspace to a Meta workspace"""

    ws_path_flag_is_user_defined = ws_path_flag is not None

    # Set a default value for the ws_path_flag
    if ws_path_flag is None:
        ws_path_flag = "./"

    # Set default value for ws_path value
    ws_path = ws_path_flag

    # Based on the definition in the annotations, we are garenteed that the first argument IS defined.
    # Check only the second argument

    if target_ws_path is None:
        # Scenario: User provided [TARGET] (subject defaults to flag/current dir)
        # If the second argument is not defined, then the first argument IS the target workspace path
        target_ws_path = target_or_subject_ws_path

    else:
        # Scenario: User provided [SUBJECT] [TARGET]
        # If the second argument has been defined, then the first one is the subject workspace path

        # If the workspace path flag was defined AND the workspace path was also defined by the user, raise an error
        if ws_path_flag_is_user_defined:
            raise ValueError(
                "Both 'ws_path_flag' and a positional 'ws-path' cannot be defined in the same command."
            )

        ws_path = target_or_subject_ws_path

    # After this line, by default the subject workspace path is
    #   the ws_path_flag if one positional arg was defined
    #   The subject workspace path is changed to positional arguments if both positional arguments were defined
    # Target workspace path is set implicitly for the single arg example, explicitly if two arguments were provided.
    # We are now garenteed a value for the subject and target workspace path after this line

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _workspace_toml_filename=ws_toml_filename,
        )
        meta_ws.unlink(
            target_workspace_path=target_ws_path,
            target_workspace_type=target_ws_type,
            _target_workspace_metadata_path=target_ws_metadata_path,
            _target_workspace_toml_filename=target_workspace_toml_filename,
        )

    if debug:
        run()
    else:
        try:
            run()
        except Exception as e:
            print(f"ERROR!: {e}")
            pass


@ovutils_wsTools_ovMeta_app.command(
    "exec", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def ovutils_wstools_meta_exec(
    ctx: typer.Context,
    identifier: str,
    identifier_type: t.Literal["id", "name"] | None = None,
    # Class init args (Standardized in all functions for a reason)
    ws_path_flag: t.Annotated[str, typer.Option("--ws-path", hidden=False)] = "./",
    ws_metadata_path: str | None = None,
    ws_toml_filename: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Executes a command to a linked OpenViatica workspace"""
    # Set a value for ws_path
    ws_path = ws_path_flag

    def run() -> None:
        meta_ws = ovutils.WorkspaceTools.MetaWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _workspace_toml_filename=ws_toml_filename,
        )
        # Get the workspace object to validate the access
        workspace_object = meta_ws.get_linked_workspace_object(
            identifier=identifier,
            identifier_type=identifier_type,
        )

        # Add the base workspace context information to the arguments if the areguments are nor blank at the moment
        if not isinstance(ovutils_wsTools_app.info.name, str):
            raise TypeError("ovutils_wsTools_app.info.name is NOT string!")

        # Default value of set_args is the app name and the workspace specifically to start with
        set_args: t.List[str] = [
            # Extract the command str from the app itself
            ovutils_wsTools_app.info.name,
            # Add at least the workspace endpoint to start with
            workspace_object.WORKSPACE_TYPE,
        ]

        # If the arguments to be passed were only help arguments, then add the help arg
        only_help_args = False
        if (len(ctx.args) == 1) and ("-h" in ctx.args or "--help" in ctx.args):
            set_args += ctx.args
            only_help_args = True

        if (len(ctx.args) == 2) and ("-h" in ctx.args and "--help" in ctx.args):
            set_args += ctx.args
            only_help_args = True

        # If there are multiple double slashes, divide between the first segment and the rest
        try:
            split_index = ctx.args.index("--")
        except ValueError:
            split_index = None
            pass

        if split_index:
            first_args = ctx.args[:split_index]
        else:
            first_args = ctx.args[:]

        # If it was not only help arguments, and there was a command there,
        # we start by adding the command that they want executed
        if not only_help_args and len(first_args) > 0:
            set_args += [ctx.args[0]]

        # If there are any arguments to be passed
        # and the command is NOT an init command
        # and the command was NOT a help command
        if len(first_args) > 0 and "init" not in first_args and not only_help_args:
            # Then inject extra ones to make the commands cwd agnostic
            # Split the first argument which is the function to be run, inject the base context, add the rest
            set_args += [
                "--ws-path",
                workspace_object.workspace_path,
                "--ws-metadata-path",
                workspace_object.workspace_metadata_path,
                "--ws-toml-filename",
                workspace_object.workspace_toml_filename,
            ]
        # If there was more than one argument, and it was not help, then we pass those at the end
        if len(first_args) > 1 and not only_help_args:
            set_args += first_args[1:]

        # Add the rest if there was a split
        if split_index:
            set_args += ctx.args[split_index:]

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
    # Initialize function args
    ws_id: str | None = None,
    ws_name: str | None = None,
    # Class init args (Standardized in all functions for a reason)
    ws_path: t.Annotated[
        str, typer.Argument(help="The path to the workspace")
    ] = "./",  # positional arg for terminal
    ws_path_flag: t.Annotated[
        str | None, typer.Option("--ws-path", hidden=True)
    ] = None,
    ws_metadata_path: str | None = None,
    ws_toml_filename: str | None = None,
    # Other args
    debug: bool = False,
) -> None:
    """Initializes a new OpenViatica Templates workspace"""
    # Set a value for ws_path based on priority system
    if ws_path_flag is not None:
        ws_path = ws_path_flag

    def run() -> None:
        templates_ws = ovutils.WorkspaceTools.TemplatesWorkspace(
            workspace_path=ws_path,
            _workspace_metadata_path=ws_metadata_path,
            _workspace_toml_filename=ws_toml_filename,
        )

        templates_ws.initialize(workspace_id=ws_id, workspace_name=ws_name)

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
