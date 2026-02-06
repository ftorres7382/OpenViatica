from OpenViatica import ovutils

def test_fibonacci_call() -> None:
    '''This function tests that the fibonacci is callable'''
    _ = ovutils.fibonacci(100)
