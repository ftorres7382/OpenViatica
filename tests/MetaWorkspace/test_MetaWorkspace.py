import pytest
import os
import shutil
from OpenViatica import ovutils

@pytest.mark.dependency()
def test_MetaWorkspace_import() -> None:
    '''Tests that OpenViatica is importable'''
    
    
    if os.path.exists("MetaWorkspace_test_dir"):
        shutil.rmtree()
    meta_ws = ovutils.WorkpaceTools.MetaWorkspace()