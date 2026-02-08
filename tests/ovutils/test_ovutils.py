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
from OpenViatica import ovutils

def test_fibonacci_call() -> None:
    '''This function tests that the fibonacci is callable'''
    _ = ovutils.fibonacci(100)

def test_fibonacci_rust_call() -> None:
    '''This function tests that the fibonacci_rust is callable'''
    _ = ovutils.fibonacci_rust(100)
