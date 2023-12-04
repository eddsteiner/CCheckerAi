use pyo3::prelude::*;
use crate::genome::{Genome, Arrays};


pub struct BCreature {
    pub genome: Genome,
    pub arrays: Arrays,
}


#[pyclass]
pub struct Creature {

}
#[pymethods]
impl Creature {
    #[new]
    fn new() -> Self {
        Creature {}
    }
}



