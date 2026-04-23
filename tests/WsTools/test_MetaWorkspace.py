import typing as t
import pytest
import os
import shutil
from OpenViatica import ovutils
from OpenViatica._general_core import General as G
from OpenViatica._types import ov_ws_types, meta_workspace_toml_type_value
from OpenViatica._core_workspaces._core_workspaces_services import \
    MetaWorkspaceService, DEFAULT_WORKSPACE_TOML_FILENAME
from OpenViatica._core_cli_interface import ovutils_wstools_meta_init

@pytest.mark.dependency()
def test_MetaWorkspace_import() -> None:
    '''Tests that OpenViatica MetaWorkspace is importable'''
    
    try:
        _ = ovutils.WorkspaceTools.MetaWorkspace
    except ImportError:
        pytest.fail("FAILED import of ovutils.WorkspaceTools.MetaWorkspace!")

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
    test_dir = "tmp/test_MetaWorkspace_init"
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
    ovutils_wstools_meta_init()

    # Check that the metadata folder has been created
    if not os.path.exists(MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH):
        pytest.fail("Default metadata folder was NOT created!")
    
    # Check that the toml also was created
    if not os.path.exists(os.path.join(
        MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH, DEFAULT_WORKSPACE_TOML_FILENAME
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
    ovutils_wstools_meta_init(
        ws_path=test_dir,
        ws_id=id_value,
        ws_name = workspace_name_value
    )

    # Check that the metadata folder has been created
    if not os.path.exists(os.path.join(
        test_dir,
        MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH
    )):
        pytest.fail("Default metadata folder was NOT created!")
    
    # Check that the toml also was created
    workspace_toml_path = os.path.join(
        test_dir, MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH, DEFAULT_WORKSPACE_TOML_FILENAME
    ) 
    if not os.path.exists(workspace_toml_path):
        pytest.fail("Default workspace toml was NOT created!")

    # Validate that it is of the correct data structure
    workspace_dict = G.read_toml_dict(
        workspace_toml_path, 
        expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE)
    workspace_dict = t.cast(ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE, workspace_dict)

    if not workspace_dict["id"] == id_value:
        pytest.fail(f"The value of the workspace id is '{workspace_dict['id']}'. It SHOULD be '{id_value}'")


    if not workspace_dict["name"] == workspace_name_value:
        pytest.fail(f"The value of the workspace id is '{workspace_dict['name']}'. It SHOULD be '{workspace_name_value}'")
    
    if not workspace_dict["type"] == meta_workspace_toml_type_value:
        pytest.fail(f"The value of the workspace id is '{workspace_dict['name']}'. It SHOULD be '{workspace_name_value}'")


    # Validate linked_by values
    expected_linked_by_value: t.List[ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE] = []
    if workspace_dict["linked_by"] != expected_linked_by_value:
        pytest.fail(f"The value of 'links_to' is '{workspace_dict['linked_by']}' expected value: '{expected_linked_by_value}'")

    # Validate links_to values
    expected_links_to_value: t.List[ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE] = []
    if workspace_dict["links_to"] != expected_links_to_value:
        pytest.fail(f"The value of 'links_to' is '{workspace_dict['links_to']}' expected value: '{expected_links_to_value}'")

    # Cleanup
    shutil.rmtree(test_dir)
