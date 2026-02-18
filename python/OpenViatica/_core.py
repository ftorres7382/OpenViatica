#
# Copyright 2026 ftorres7382
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.#


from . import _rs_core
from typeguard import typechecked
class ovutils:
    '''
    # ovutils
    This class is used to create and manage a data analysis workspace

    ## Import
    ```from OpenViatica import ovutils```

    ## Functions
    1. fibonacci(n: int) -> int
    2. fibonacci_rust(n:int) -> int
    '''
    @staticmethod
    @typechecked
    def fibonacci(n: int) -> int:
        '''Calculates fibonacci numbers without recursion'''
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    

    @staticmethod
    @typechecked
    def fibonacci_rust(n:int) -> int:
        '''Calculates fibonacci numbers without recursion using rust'''
        result = _rs_core.fibonacci(n)
        result = int(result)
        return result
    