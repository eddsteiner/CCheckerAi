use std::slice;

use pyo3::prelude::*;
use crate::genome::{Genome, Arrays};


extern {
    /// Calculates the output of the given neural network arrays, on CUDA
    fn calculate(
        mult: *const f32,
        source: *const u32,
        dest: *const u32,
        output: *mut f32,
        mult_threads: *const u32,
        output_threads: *const u32,

        connections_size: u32,
        output_size: u32,
        threads_size: u32,
    );
}


#[derive(Clone)]
pub struct BCreature {
    pub genome: Genome,
    pub arrays: Arrays,
}


#[pyclass]
pub struct Creature {
    pub arrays: Arrays,
    pub input_size: usize,
    #[pyo3(get)]
    pub node_count: usize,
    #[pyo3(get)]
    pub connection_count: usize,
}
#[pymethods]
impl Creature {

    /// Accepts a pointer to a board and returns the calculated confidences for each move
    pub fn calculate(&mut self, board_pointer: usize, output_pointer: usize) {
        // first we need to copy the values to our output vector
        let board = unsafe { slice::from_raw_parts_mut(board_pointer as *mut f32, self.input_size) };
        let output = unsafe { slice::from_raw_parts_mut(output_pointer as *mut f32, 417) };
        for i in 0..self.input_size {
            self.arrays.output[i+1] = board[i];
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

            self.arrays.multiplier.len() as u32,
            self.arrays.output.len() as u32,
            self.arrays.mult_threads.len() as u32,
        )};

        // push output values to buffer
        for i in 0..417 {
            output[i] = self.arrays.output[(self.arrays.output.len()-417)+i];
        }
    }
}
impl Creature {
    pub fn from(arrays: Arrays, input_size: usize, node_count: usize, connection_count: usize) -> Self {
        Creature { arrays, input_size, node_count, connection_count }
    }
}




