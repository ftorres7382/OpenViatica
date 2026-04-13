import pytest
import os
import shutil
from OpenViatica import ovutils
from OpenViatica._core_workspaces._core_workspaces_services import MetaWorkspaceService

@pytest.mark.dependency()
def test_MetaWorkspace_import() -> None:
    '''Tests that OpenViatica MetaWorkspace is importable'''
    
    try:
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
            5. Redo all the tests but doing terminal commands
    
    It will not test anything that is NOT user facing, ONLY user facing functions and variables will be tested
    
    '''
    test_dir = "test_MetaWorkspace_auto"
    # Reset dir
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    og_cwd = os.getcwd()

    os.chdir(test_dir)

    # test default behaviour
    meta_ws = ovutils.WorkpaceTools.MetaWorkspace()
    meta_ws.initialize()

    # Check that the metadata folder has been created
    if not os.path.exists(MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH):
        pytest.fail("Default metadata folder was NOT created!")
    
    os.chdir(og_cwd)
    shutil.rmtree(test_dir)

    
