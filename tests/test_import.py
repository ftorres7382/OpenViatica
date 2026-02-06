from tokenize import OP
import pytest
def test_OpenViatica_import() -> None:
    '''Tests that OpenViatica is importable'''
    try:
        import OpenViatica
        # using is to make the linter happy
        _ = OpenViatica.__doc__
    except ImportError:
        pytest.fail("FAILED OpenViatica import!")
    
def test_ovutils_import() -> None:
    '''Tests that the ovutils is importable'''