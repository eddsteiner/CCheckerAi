use std::slice;

use pyo3::prelude::*;
use crate::genome::{Genome, Arrays};


extern {
    fn calculate(
        mult: *const f32,
        source: *const usize,
        dest: *const usize,
        output: *mut f32,
        mult_threads: *const usize,
        output_threads: *const usize,
    );
}


pub struct BCreature {
    pub genome: Genome,
    pub arrays: Arrays,
}


#[pyclass]
pub struct Creature {
    pub arrays: Arrays,
    pub input_size: usize,
}
#[pymethods]
impl Creature {

    pub fn calculate(&mut self, pointer: usize) -> PyResult<usize> {
        // first we need to copy the values to our output vector
        let board = unsafe { slice::from_raw_parts_mut(pointer as *mut i32, self.input_size) };
        for i in 0..self.input_size {
            self.arrays.output[i+1] = board[i] as f32;
        }

        // clean up all node values (except the bias since that should never change)
        for i in self.input_size+1..self.arrays.output.len() {
            self.arrays.output[i] = 0.0;
        }

        unsafe { calculate(
            self.arrays.multiplier.as_ptr(),
            self.arrays.source.as_ptr(),
            self.arrays.dest.as_ptr(),
            self.arrays.output.as_mut_ptr(),
            self.arrays.mult_threads.as_ptr(),
            self.arrays.output_threads.as_ptr(),
        )};

        Ok(self.arrays.output.as_ptr() as usize)
    }
}
impl Creature {
    pub fn from(arrays: Arrays, input_size: usize) -> Self {
        Creature { arrays, input_size }
    }
}
//impl ToPyObject for Creature {
//    fn to_object(&self, py: Python<'_>) -> PyObject {
//        //self.to_object(py)
//    }
//}



