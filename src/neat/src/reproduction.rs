use std::collections::HashSet;

use crate::genome::{Genome, ConnectionGene, NodeGene, Arrays};
use rand::Rng;


/// Used during reproduction to keep track of an innovation
struct Innov {
    innov: usize,
    in_node: usize,
    out_node: usize,
}


/// Facilitates genome reproduction
pub struct ReproductionHelper {
    pub innov: usize,
    pub id: usize,
}
impl ReproductionHelper {
    /// Creates a new ReproductionHelper with the given global innov number
    pub fn new(innov: usize, id: usize) -> Self {
        ReproductionHelper { innov, id }
    }

    /// Creates a child genome from two parent genomes
    pub fn reproduce(&self, parent1: &Genome, parent2: &Genome) -> Genome {
        let mut new_genome: Genome = Genome {
            nodes: Vec::new(),
            connections: Vec::new(),
            input_ids: HashSet::new(),
            output_ids: HashSet::new(),
        };
        let mut id_set = HashSet::new();
        let mut rng = rand::thread_rng();
        let mut index1 = 0; //index in parent1's list
        let mut index2 = 0; //index in parent2's list

        // first add the connections
        let max_innov = parent1.connections[parent1.connections.len()-1].innov
            .max(parent2.connections[parent2.connections.len()-1].innov);
        for innov in 0..max_innov { //go through each innov, see if either parent has it
            let in1 = //does parent1 contain this innov?
                if parent1.connections[index1].innov == innov {
                    index1 += 1; //increment parent1 because we covered one of its genes
                    true
                } else {
                    false
                };
            let in2 = //does parent2?
                if parent2.connections[index2].innov == innov {
                    index2 += 1; 
                    true
                } else {
                    false
                };
            if !in1 || !in2 { //neither contain this innov
                continue;
            }
            let mut new_gene: ConnectionGene; //centralized declaration instead of in the if nest
            if in1 && in2 { //both contain a gene, push it
                new_gene = parent1.connections[index1-1].clone();
                let distance = (parent1.connections[index1-1].weight - parent2.connections[index2-1].weight).abs() / 2.0;
                let center = parent1.connections[index1-1].weight / 2.0 + parent2.connections[index2-1].weight / 2.0;
                new_gene.weight = rng.gen_range(center-distance..center+distance); //possible range for the mutated weight
            } else if in1 { //just parent1 contains a gene
                if rng.gen_bool(0.5) { //50% chance of not adding the gene
                    continue;
                }
                new_gene = parent1.connections[index1].clone();
            } else { //just parent2 contains a gene
                if rng.gen_bool(0.5) { //50% chance of not adding the gene
                    continue;
                }
                new_gene = parent2.connections[index2].clone();
            }
            if rng.gen_bool(0.25) { //25% of flipping status of a connection
                new_gene.enabled = !new_gene.enabled;
            }
            //new_genome.input_ids.insert(new_gene.in_node); //update child nodes
            //new_genome.output_ids.insert(new_gene.out_node); //update child nodes
            id_set.insert(new_gene.in_node); //for generating all nodes later
            id_set.insert(new_gene.out_node);
            new_genome.connections.push(new_gene); //add the new connection to the child
        }


        // update the input and output ids, both parents should have the same
        //new_genome.input_ids.union(&parent1.input_ids);
        //new_genome.input_ids.union(&parent2.input_ids);
        //new_genome.output_ids.union(&parent1.output_ids);
        //new_genome.output_ids.union(&parent2.output_ids);
        new_genome.input_ids = parent1.input_ids.clone();
        new_genome.output_ids = parent1.output_ids.clone();

        // now that we've added all connections, add the nodes
        let max_id = parent1.nodes[parent1.nodes.len()-1].id
            .max(parent2.nodes[parent2.nodes.len()-1].id);
        for i in 0..max_id { //this slower method ensures all nodes are in order
            if id_set.contains(&i) { //this node is used
                new_genome.nodes.push(NodeGene { id: i, node_type: 0 })
            }
        }
        
        new_genome
    }


    // Takes an existing genome and mutates it
    pub fn mutate(&mut self, genome: &mut Genome) {
        let mut rng = rand::thread_rng();
        let num_add_mutations = //number of connections to add, if any are available
            if rng.gen_bool(0.15) {
                if rng.gen_bool(0.3) {
                    if rng.gen_bool(0.5) {
                        3
                    } else {
                        2
                    }
                } else {
                    1
                }
            } else {
                0
            };

        let num_split_mutations = //number of connections to split
            if rng.gen_bool(0.15) {
                if rng.gen_bool(0.3) {
                    if rng.gen_bool(0.5) {
                        3
                    } else {
                        2
                    }
                } else {
                    1
                }
            } else {
                0
            };
        
        for _ in 0..num_add_mutations { //find a set of two nodes that are currently unconnected
            let (bucket_labels, buckets, _, _, _) = Arrays::to_buckets(genome).unwrap();
            //if buckets.contains_key(k)
            // grab any node and see if its bucket is the same size as all nodes

            
        }

        for _ in 0..num_add_mutations { //split any connection
            
        }

        todo!()
    }
}



