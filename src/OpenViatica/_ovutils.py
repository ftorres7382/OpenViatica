class ovutils:
    '''
    # ovutils
    This class is used to create and manage a data analysis workspace
    '''
    @staticmethod
    def fibonacci(n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    