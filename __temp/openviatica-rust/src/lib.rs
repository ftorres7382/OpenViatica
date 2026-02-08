/*
 * Copyright 2026 ftorres7382
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */
use pyo3::prelude::*;

/// This function is exposed to Python
#[pyfunction]
fn fibonacci(n: u32) -> PyResult<u128> {
    let mut a: u128 = 0;
    let mut b: u128 = 1;

    for _ in 0..n {
        let temp = a;
        a=b;
        // Use the checked_add
        match temp.checked_add(b){
            // If there is any value, set be as the new value
            Some(result_val) => b = result_val,
            // If there was no value, that means overflow
            None => return Err(
                pyo3::exceptions::PyOverflowError::new_err("Fibonacci overflowed u128")
            ),
        }
    }

    Ok(a)
}

/// This defines the actual Python module
#[pymodule]
fn openviatica_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    Ok(())
}