use pyo3::prelude::*;
use std::slice;

mod genome;
mod creature;
mod generation_manager;
mod reproduction;

use creature::Creature;
use generation_manager::GenerationManager;


extern { fn maxmul(a: *const f32, b: *const f32, c: *mut f32, size: i32) -> (); }


/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


#[pyfunction]
fn test_cuda() -> PyResult<()> {
    let a: Vec<f32> = vec![-1.0, 2.0, 4.0, 0.0, 5.0, 3.0, 6.0, 2.0, 1.0];
    let b: Vec<f32> = vec![3.0, 0.0, 2.0, 3.0, 4.0, 5.0, 4.0, 7.0, 2.0];
    let mut c: Vec<f32> = vec![0.0; 9];
    let a_point = a.as_ptr() as *const f32;
    let b_point = b.as_ptr() as *const f32;
    let c_point = c.as_mut_ptr() as *mut f32;

    unsafe { maxmul(a_point, b_point, c_point, 3) };

    println!("{:?}", c);
    Ok(())
}


#[pyfunction]
fn test_pointer(pointer: i64, length: usize) -> PyResult<()> {
    //let mut a: *mut [i32] = pointer as *mut [i32];
    let a = unsafe { slice::from_raw_parts_mut(pointer as *mut i32, length) };
    a[3] = 30;
    println!("{:?}", a);
    Ok(())
}


#[pyfunction]
fn cu_maxmul(a: i64, b: i64, c: i64, size: usize) -> PyResult<()> {
    unsafe { maxmul(a as *mut f32, b as *mut f32, c as *mut f32, size as i32) };
    Ok(())
}


/// A Python module implemented in Rust.
#[pymodule]
fn neat(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(test_cuda, m)?)?;
    m.add_function(wrap_pyfunction!(test_pointer, m)?)?;
    m.add_function(wrap_pyfunction!(cu_maxmul, m)?)?;
    m.add_class::<Creature>()?;
    m.add_class::<GenerationManager>()?;
    Ok(())
}


