import tomlkit
import pytest
import os
import shutil
from OpenViatica._core_cli_interface import ovutils_init
from OpenViatica._core_workspaces._core_workspaces_services import \
    MetaWorkspaceService, DEFAULT_WORKSPACE_TOML_FILENAME

@pytest.mark.dependency()
def test_ovutils_import() -> None:
    '''Tests that OpenViatica MetaWorkspace is importable'''
    
    try:
        from OpenViatica import ovutils
        _ = ovutils.WorkpaceTools.MetaWorkspace
    except ImportError:
        pytest.fail("FAILED import of ovutils.WorkpaceTools.MetaWorkspace!")

def test_MetaWorkspace_initialize() -> None:
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
    # Import internally since we do not know until the tests run if it can be imported
    from OpenViatica import ovutils

    test_dir = "tmp/test_openviatica_init"
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
    ovutils_init()

    # Check that the metadata folder has been created
    if not os.path.exists(ovutils.DEFAULT_METADATA_FOLDERPATH):
        pytest.fail("Default metadata folder was NOT created!")
    
    # Check that the meta workspace metadata folder was created
    if not os.path.exists(os.path.join(
        ovutils.DEFAULT_METADATA_FOLDERPATH, MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH
    )):
        pytest.fail("Meta worksapace metadata folder was NOT created!")
    
    # Go back and redo while changing all the user parameters
    os.chdir(og_cwd)
    shutil.rmtree(test_dir)

    ####################
    # Test 2
    ####################
    os.mkdir(test_dir)

    id_value = "test_id"
    workspace_name_value = "test_name"
    ovutils_init(
        ws_path=test_dir,
        ws_id=id_value,
        ws_name = workspace_name_value
    )

    # Check that the metadata folder has been created
    if not os.path.exists(os.path.join(
        test_dir,
        ovutils.DEFAULT_METADATA_FOLDERPATH
    )):
        pytest.fail("Default openviatica metadata folder was NOT created!")
    
    # Check that the Meta workspace metadata folder also was created
    meta_workspace_metadata_path = os.path.join(
        test_dir,
        ovutils.DEFAULT_METADATA_FOLDERPATH,
        MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH
    ) 
    if not os.path.exists(meta_workspace_metadata_path):
        pytest.fail("Default meta workspace metadata folder was NOT created!")

    # Check that the meta workspace toml has been created
    workspace_toml_path = os.path.join(
        test_dir, 
        ovutils.DEFAULT_METADATA_FOLDERPATH, 
        MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH, 
        DEFAULT_WORKSPACE_TOML_FILENAME
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
