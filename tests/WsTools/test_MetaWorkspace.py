from inspect import unwrap
import typing as t
import pytest
import os
import shutil
from OpenViatica import ovutils
from OpenViatica._general_core import General as G
from OpenViatica._types import ov_ws_types, meta_workspace_toml_type_value
from OpenViatica._core_workspaces._core_workspaces_services import \
    MetaWorkspaceService, DEFAULT_WORKSPACE_TOML_FILENAME
from OpenViatica._core_cli_interface import ovutils_wstools_meta_init, ovutils_wstools_meta_link

@pytest.mark.dependency()
def test_MetaWorkspace_import() -> None:
    '''Tests that OpenViatica MetaWorkspace is importable'''
    
    try:
        _ = ovutils.WorkspaceTools.MetaWorkspace
    except ImportError:
        pytest.fail("FAILED import of ovutils.WorkspaceTools.MetaWorkspace!")

@pytest.mark.dependency(depends=["test_MetaWorkspace_import"])
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
    os.chdir(og_cwd)


@pytest.mark.dependency(depends=["test_MetaWorkspace_initialize"])
def test_MetaWorkspace_link() -> None:
    ''' 
    Initializes two meta workspaces, then tires to link them, them removes it 
    
    '''

    test_dir = "tmp/test_MetaWorkspace_link"
    # Reset dir
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    og_cwd = os.getcwd()

    ####################
    # Test 1
    ####################
    os.chdir(test_dir)

    # Create extra dir for other workspace
    os.mkdir("meta-ws2")

    # Initialize two meta workspace
    ovutils_wstools_meta_init()

    ovutils_wstools_meta_init(ws_path="meta-ws2")

    # Link them both together
    ovutils_wstools_meta_link("meta-ws2", "ov-meta")

    # Check that the added entries are exactly the correct format and values
    expected_workspace_toml_path = ".ov-meta/workspace.toml"
    expected_workspace_toml_path2 = "meta-ws2/.ov-meta/workspace.toml"

    # Read both of them and validate the format
    workspace_toml_doc = G.read_toml_doc(
        toml_filepath=expected_workspace_toml_path,
        expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
    )
    workspace_toml_doc2 = G.read_toml_doc(
        toml_filepath=expected_workspace_toml_path2,
        expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
    )

    # Validate the links_to and linked_by values
    linked_by_value = workspace_toml_doc2.unwrap()["linked_by"][0]
    workspace_toml_dict = t.cast(
        ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
        workspace_toml_doc.unwrap()
    )
    expected_linked_by_value: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
        "id": workspace_toml_dict["id"],
        "name": workspace_toml_dict["name"],
        "type": workspace_toml_dict["type"],
        "workspace_tomlpath": os.path.abspath(expected_workspace_toml_path)
    } 
    if linked_by_value != expected_linked_by_value:
        pytest.fail(f"The expected linked_by value is '{expected_linked_by_value}' but found '{linked_by_value}' instead.") 

    # Validate the links_to and linked_by values
    links_to_value = workspace_toml_doc.unwrap()["links_to"][0]
    workspace_toml_dict2 = t.cast(
        ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
        workspace_toml_doc2.unwrap()
    )
    expected_links_to_value: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
        "id": workspace_toml_dict2["id"],
        "name": workspace_toml_dict2["name"],
        "type": workspace_toml_dict2["type"],
        "workspace_tomlpath": os.path.abspath(expected_workspace_toml_path2)
    } 
    if links_to_value != expected_links_to_value:
        pytest.fail(f"The expected links_to value is '{expected_links_to_value}' but found '{links_to_value}' instead.") 

    # Go back and redo while changing all the user parameters
    os.chdir(og_cwd)
    shutil.rmtree(test_dir)

    ####################
    # Test 2
    ####################
    os.mkdir(test_dir)

    # Create extra dir for other workspace
    ws_path2 = os.path.join(test_dir,"meta-ws2")
    os.mkdir(ws_path2)

    # Re-initialize defining the values for workspace paths
    ovutils_wstools_meta_init(ws_path = test_dir)

    ovutils_wstools_meta_init(ws_path = ws_path2)

    # Re-link while defining as many user variables as possible
    ovutils_wstools_meta_link(
        subject_ws_path=test_dir,
        target_ws_path= ws_path2,
        target_ws_type="ov-meta"
    )
    # Again, should probably test with other ws types but levaing it as is for now

    # Validate the results
    # Check that the added entries are exactly the correct format and values
    expected_workspace_toml_path = os.path.join(test_dir, ".ov-meta/workspace.toml")
    expected_workspace_toml_path2 = os.path.join(ws_path2, ".ov-meta/workspace.toml")

    # Read both of them and validate the format
    workspace_toml_doc = G.read_toml_doc(
        toml_filepath=expected_workspace_toml_path,
        expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
    )
    workspace_toml_doc2 = G.read_toml_doc(
        toml_filepath=expected_workspace_toml_path2,
        expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
    )

    # Validate the links_to and linked_by values
    linked_by_value = workspace_toml_doc2.unwrap()["linked_by"][0]
    workspace_toml_dict = t.cast(
        ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
        workspace_toml_doc.unwrap()
    )
    expected_linked_by_value = {
        "id": workspace_toml_dict["id"],
        "name": workspace_toml_dict["name"],
        "type": workspace_toml_dict["type"],
        "workspace_tomlpath": os.path.abspath(expected_workspace_toml_path)
    } 
    if linked_by_value != expected_linked_by_value:
        pytest.fail(f"The expected linked_by value is '{expected_linked_by_value}' but found '{linked_by_value}' instead.") 

    # Validate the links_to and linked_by values
    links_to_value = workspace_toml_doc.unwrap()["links_to"][0]
    workspace_toml_dict2 = t.cast(
        ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
        workspace_toml_doc2.unwrap()
    )
    expected_links_to_value = {
        "id": workspace_toml_dict2["id"],
        "name": workspace_toml_dict2["name"],
        "type": workspace_toml_dict2["type"],
        "workspace_tomlpath": os.path.abspath(expected_workspace_toml_path2)
    } 
    if links_to_value != expected_links_to_value:
        pytest.fail(f"The expected links_to value is '{expected_links_to_value}' but found '{links_to_value}' instead.") 



    # Cleanup
    shutil.rmtree(test_dir)
    os.chdir(og_cwd)