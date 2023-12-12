use core::slice;
use std::collections::HashSet;

use pyo3::{prelude::*, types::PyList};
use rand::{Rng, seq::SliceRandom};
use crate::{creature::{BCreature, Creature}, genome::{NodeGene, ConnectionGene, Genome, Arrays}, reproduction::ReproductionHelper};

#[pyclass]
pub struct GenerationManager {
    #[pyo3(get)]
    
    population_size: usize,
    input_count: usize, //true input count (excluding bias)
    output_count: usize,
    population: Vec<BCreature>,
    reproduction_helper: ReproductionHelper,
}
#[pymethods]
impl GenerationManager {
    #[new]
    pub fn new(population_size: i64, input_count: i64, output_count: i64) -> Self {
        //let generation_size = generation_size as u32;
        //let input_count = input_count as u32;
        //let output_count = output_count as u32;
        let mut gen_man = GenerationManager {
            
            population_size: population_size as usize,
            input_count: input_count as usize,
            output_count: output_count as usize,
            //input_ids: (0..input_count).collect(),
            //output_ids: (input_count..input_count+output_count).collect(),
            population: Vec::new(),
            reproduction_helper: ReproductionHelper::new(0, 0),
        };
        gen_man.fresh_generation();
        gen_man
    }

    pub fn get_current_generation<'a>(&'a self, py: Python<'a>) -> PyResult<&PyList> {
        let list: &PyList = PyList::new(py, [0; 0]);

        // convert each BCreature into a Python Creature
        for i in 0..self.population_size {
            let arrs = self.population[i].arrays.clone();
            let node_count = self.population[i].genome.nodes.len();
            let connection_count = self.population[i].genome.connections.len();
            list.append(Creature::from(arrs, self.input_count, node_count, connection_count).into_py(py))?; //convert arrs into a Creature then into a Python object
        }

        Ok(list)
    }

    pub fn evolve(&mut self, rankings_pointer: usize) {
        let rankings = unsafe { slice::from_raw_parts_mut(rankings_pointer as *mut i32, self.population_size) };
        let mut ranked_population = Vec::with_capacity(self.population_size);
        for i in 0..self.population_size { //attach the rankings to the creatures
            ranked_population.push((rankings[i], i));
        }

        // kill half the population
        ranked_population.sort_by(|x, y| x.0.cmp(&y.0)); //sort creature indices by their fitness
        let order: Vec<usize> = ranked_population.iter().map(|x| x.1).collect(); //ordered indices
        let new_population: Vec<BCreature> = order[0..self.population.len()/2].iter().map(|x| self.population[*x].clone()).collect();

        // for each open space
        let mut rng = rand::thread_rng();
        for _ in 0..self.population.len()-new_population.len() {
            let creature1 = new_population.choose(&mut rng).unwrap(); //safe unwrap
            let creature2 = new_population.choose(&mut rng).unwrap(); //safe unwrap

            // breed these two creatures until they create a valid baby
            let mut new_genome = self.reproduction_helper.reproduce(&creature1.genome, &creature2.genome);
            self.reproduction_helper.mutate(&mut new_genome);
            let arrays: Arrays;
            loop {
                match Arrays::from_genome(&new_genome) {
                    Some(x) => {
                        arrays = x;
                        break;
                    },
                    None => {
                        new_genome = self.reproduction_helper.reproduce(&creature1.genome, &creature2.genome);
                        self.reproduction_helper.mutate(&mut new_genome);
                    }
                }
            }

            // build a creature from the genome
            //let arrays = Arrays::from_genome(&new_genome).unwrap(); //convert the newly created genome into an Arrays struct
            self.population.push(BCreature {genome: new_genome, arrays: arrays}); //push to the population

        }

        // push the new population back to the generation manager
        self.population = new_population;
    }
}
impl GenerationManager {
    fn fresh_generation(&mut self) {
        self.population = Vec::with_capacity(self.population_size);
        let mut rng = rand::thread_rng(); //for random things

        for _ in 0..self.population_size { //for each creature
            let mut genome = Genome::with_capacities((self.input_count + 1) + self.output_count, (self.input_count + 1) * self.output_count + 1); //include bias
            
            // create input nodes
            genome.input_ids = HashSet::with_capacity(self.input_count+1);
            for j in 0..self.input_count+1 {
                genome.nodes.push(NodeGene { id: j, node_type: 0 });
                genome.input_ids.insert(j);
                
            }

            // create output nodes and connections
            genome.output_ids = HashSet::with_capacity(self.output_count);
            //for j in (self.input_count+1)..(self.input_count+1)+self.output_count { //for every output node
            for j in 0..self.output_count { //for every output node
                let output_id = j + self.input_count + 1; //need to offset by the number of input ids
                genome.nodes.push(NodeGene { id: output_id, node_type: 1});
                genome.output_ids.insert(output_id);

                // attach this output node to each input node
                for k in 0..(self.input_count+1) { //for every input node
                    genome.connections.push(ConnectionGene { //create connection between input and output node
                        in_node: k,
                        out_node: output_id,
                        weight: rng.gen_range(-5.0..5.0), //randomized weight
                        enabled: rng.gen_bool(0.5), //randomized enabledness
                        innov: k + j * (self.input_count+1), //each connection has a unique id
                    });
                }
            }
            
            self.reproduction_helper.innov = (self.input_count+1) * self.output_count; //number of connections
            self.reproduction_helper.id = (self.input_count+1) + self.output_count; //number of nodes

            // NOTE: we can unwrap here because we know it will always be valid, it does not have cycles
            let arrays = Arrays::from_genome(&genome).unwrap(); //convert the newly created genome into an Arrays struct
            self.population.push(BCreature {genome, arrays}); //push to the population
        }
    }
}



