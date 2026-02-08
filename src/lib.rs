use pyo3::prelude::*;

/// A simple function coded in Rust
#[pyfunction]
fn fibonacci(n: u32) -> u128 {
    let mut a: u128 = 0;
    let mut b: u128 = 1;
    
    for _ in 0..n {
        let temp = a;
        a = b;
        b = temp + b;
    }
    a
}

/// The OpenViatica Rust module
#[pymodule]
fn _openviatica_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    Ok(())
}