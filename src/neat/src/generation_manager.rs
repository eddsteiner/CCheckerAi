use std::collections::HashSet;

use pyo3::prelude::*;
use rand::Rng;
use crate::{creature::{BCreature, Creature}, genome::{NodeGene, ConnectionGene, Genome, Arrays}};

#[pyclass]
pub struct GenerationManager {
    #[pyo3(get)]
    population_size: usize,
    input_count: usize, //true input count (excluding bias)
    output_count: usize,
    population: Vec<BCreature>,
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
        };
        gen_man.fresh_generation();
        gen_man
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
            for j in self.input_count..(self.input_count+1)+self.output_count { //for every output node
                genome.nodes.push(NodeGene { id: j, node_type: 1});
                genome.output_ids.insert(j);

                // attach this output node to each input node
                for k in 0..(self.input_count+1) { //for every input node
                    genome.connections.push(ConnectionGene { //create connection between input and output node
                        in_node: k,
                        out_node: j,
                        weight: rng.gen_range(-5.0..5.0), //randomized weight
                        enabled: rng.gen_bool(0.5), //randomized enabledness
                        innov: k,
                    });
                }
            }

            // NOTE: we can unwrap here because we know it will always be valid, it does not have cycles
            let arrays = Arrays::from_genome(&genome).unwrap(); //convert the newly created genome into an Arrays struct
            self.population.push(BCreature {genome, arrays}); //push to the population
        }
    }
}



