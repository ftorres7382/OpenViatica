import tomlkit
import pytest
import os
import shutil
from OpenViatica import ovutils
from OpenViatica._core_workspaces._core_workspaces_services import \
    TemplatesWorkspaceService, DEFAULT_WORKSPACE_TOML_FILENAME
from OpenViatica._core_cli_interface import ovutils_wstools_templates_init

@pytest.mark.dependency()
def test_TemplatesWorkspace_import() -> None:
    '''Tests that OpenViatica TemplatesWorkspace is importable'''
    
    try:
        _ = ovutils.WorkspaceTools.TemplatesWorkspace
    except ImportError:
        pytest.fail("FAILED import of ovutils.WorkspaceTools.TemplatesWorkspace!")

def test_TemplatesWorkspace_initialize() -> None:
    '''
    Tests that the initialize function in the MetWorkspace tool functions properly
    
    It will create a test folder and then will test the following:
        1. Default behaviour: 
            1. When cd into the test folder, it should run the initialize() without any problems
            2. If I try to run the init a second time, it should give me a specific error
            3. If I reset the test folder, then I should be able to define the workspace path and redo the same steps
            4. Check each of the user facing config in the initialize function
    
    It will not test anything that is NOT user facing, ONLY user facing functions and variables will be tested
    
    '''
    test_dir = "tmp/test_TemplatesWorkspace_init"
    # Reset dir
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    og_cwd = os.getcwd()

    ####################
    # Test 1
    ####################
    os.chdir(test_dir)

    # test default behaviour
    # By calling the terminal, we should be able to test the terminal and class at the same time
    # Also the terminal will be the primary way some users interact with the tool
    ovutils_wstools_templates_init()

    # Check that the metadata folder has been created
    if not os.path.exists(TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH):
        pytest.fail("Default metadata folder was NOT created!")
    
    # Check that the toml also was created
    if not os.path.exists(os.path.join(
        TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH, DEFAULT_WORKSPACE_TOML_FILENAME
    )):
        pytest.fail("Default workspace toml was NOT created!")
    
    # Go back and redo while changing all the user parameters
    os.chdir(og_cwd)
    shutil.rmtree(test_dir)

    ####################
    # Test 2
    ####################
    os.mkdir(test_dir)

    id_value = "test_id"
    workspace_name_value = "test_name"
    ovutils_wstools_templates_init(
        ws_path=test_dir,
        ws_id=id_value,
        ws_name = workspace_name_value
    )

    # Check that the metadata folder has been created
    if not os.path.exists(os.path.join(
        test_dir,
        TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH
    )):
        pytest.fail("Default metadata folder was NOT created!")
    
    # Check that the toml also was created
    workspace_toml_path = os.path.join(
        test_dir, TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH, DEFAULT_WORKSPACE_TOML_FILENAME
    ) 
    if not os.path.exists(workspace_toml_path):
        pytest.fail("Default workspace toml was NOT created!")

    # Check the value of the workspace toml
    with open(workspace_toml_path, mode="rt") as f:
        doc = tomlkit.parse(f.read())
    
    if not doc["id"] == id_value:
        pytest.fail(f"The value of the workspace id is '{doc['id']}'. It SHOULD be '{id_value}'")


    if not doc["name"] == workspace_name_value:
        pytest.fail(f"The value of the workspace id is '{doc['workspace_name']}'. It SHOULD be '{workspace_name_value}'")

    # Cleanup
    shutil.rmtree(test_dir)
