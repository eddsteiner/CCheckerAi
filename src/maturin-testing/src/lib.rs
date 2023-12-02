use pyo3::prelude::*;

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
    let a_point = a.as_slice().as_ptr() as *const f32;
    let b_point = b.as_slice().as_ptr() as *const f32;
    let c_point = c.as_mut_slice().as_mut_ptr() as *mut f32;

    println!("waddup");
    unsafe { maxmul(a_point, b_point, c_point, 3) };

    println!("{:?}", c);

    /*
       a = np.array([-1, 2, 4, 0, 5, 3, 6, 2, 1], dtype = np.float32)
        b = np.array([3, 0, 2, 3, 4, 5, 4, 7, 2], dtype = np.float32)
       */

    //let x = 
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn maturin_testing(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(test_cuda, m)?)?;
    Ok(())
}
