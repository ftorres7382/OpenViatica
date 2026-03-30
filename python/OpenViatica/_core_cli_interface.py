# '''
# The purpose of the _cli_interface is to map all the functions the user invokes through the CLI 
# to the appropriate user facing module and function.

# The main function will be invokeable through the ovutils keyword  
# '''
# # TODO:

# # README.md not intuitive enough, find another filename that screams click and read me please
#     # SECTION_PURPOSE.md
#     # HOW_TO_GET_STARTED.md
# # Make the purpose of the Docs folder more apparent
# # Home
# # make purpose of each folder more clear, especially repos
# import typer
# from ._core_ovutils import ovutils

# app = typer.Typer(
#     help="OpenVitaca Utilities ('ovutils'): A workspace creation and management engine\n\nGETTING STARTED:\nRun the command inside the quotes: 'ovutils ws init'",
#     add_completion=False,
#     context_settings={"help_option_names": ["-h", "--help"]}
#     )
# # Creating an alias for better organization
# ovutils_app = app

# # Create the ws app and add to the set of commands that can be done
# ovutils_ws_app = typer.Typer(
#     help="'ovutils ws': Creates & manages OpenViatica DATA Workspaces."
#     )
# ovutils_app.add_typer(ovutils_ws_app, name="ws")

# # Create the templates app & add to ovutils
# ovutils_templates_app  = typer.Typer(
#     help="'ovutils tmpl': Creates & manages OpenViatica TEMPLATE Workspaces."
# )
# ovutils_app.add_typer(ovutils_templates_app, name="tmpl")



# # ws Routing
# @ovutils_ws_app.command("init")
# def ovutils_ws_init(
#     workspace_id:str | None = None, 
#     workspace_name: str | None = None,
#     create_new_directory:bool = False, 
#     uuid_dirname:bool = False,
#     ask_dir_cleanup: bool = True,
#     dirpath:str | None = None,
#     workspace_dirname:str | None = None, 
# ) -> None:
#     '''Initializes a new OpenViatica DATA workspace'''
#     ovutils.workspace.init(
#             workspace_id, 
#             workspace_name,
#             create_new_directory,
#             uuid_dirname,
#             ask_dir_cleanup, 
#             dirpath,
#             workspace_dirname,
#     )

# # templates Routing
# @ovutils_templates_app.command("init")
# def init(
#     metadata_dirpath:str = ovutils.templates.default_metadata_dirpath,
#     workspace_id:str | None = None, 
#     workspace_name: str | None = ovutils.templates.default_metadata_dirpath
# ) -> None:
#     '''Initializes a new TEMPLATES workspace'''
#     templates_obj = ovutils.templates(metadata_dirpath = metadata_dirpath)
    
#     # Try and Except so that upon error it does NOT show the traceback to the user
#     try:
#         templates_obj.init_workspace(
#             workspace_id = workspace_id,
#             workspace_name = workspace_name
#         )
#     except Exception as e:
#         print(e)



# # Default callbacks for whenever the tool is called without any arguments
# @ovutils_app.callback(invoke_without_command=True)
# def main(ctx: typer.Context) -> None:
#     """
#     OpenViatica Utilities CLI.
#     """
#     if ctx.invoked_subcommand is None:
#         # This prints the help menu to the console
#         typer.echo(ctx.get_help())
#         # This exits the program gracefully
#         raise typer.Exit()

# @ovutils_ws_app.callback(invoke_without_command=True)
# def ws_main(ctx: typer.Context) -> None:
#     """
#     OpenViatica Utilities CLI.
#     """
#     if ctx.invoked_subcommand is None:
#         # This prints the help menu to the console
#         typer.echo(ctx.get_help())
#         # This exits the program gracefully
#         raise typer.Exit()

# @ovutils_templates_app.callback(invoke_without_command=True)
# def templates_main(ctx: typer.Context) -> None:
#     """
#     OpenViatica Utilities CLI.
#     """
#     if ctx.invoked_subcommand is None:
#         # This prints the help menu to the console
#         typer.echo(ctx.get_help())
#         # This exits the program gracefully
#         raise typer.Exit()

# if __name__ == "__main__":
#     app()