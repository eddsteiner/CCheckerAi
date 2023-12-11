use std::collections::{HashSet, HashMap};

use crate::genome::{Genome, ConnectionGene, NodeGene, Arrays};
use rand::{Rng, seq::SliceRandom};


/// Used during reproduction to keep track of an innovation
#[derive(PartialEq, Eq, Hash)]
pub struct Innov {
    pub in_node: usize,
    pub out_node: usize,
    pub split: bool, //specifies whether the two nodes were split or whether a connection was added
    //pub innov: usize, //contains the innov for the new connection if no split, or the innov for the first connection and +1 for the second one
}


/// Facilitates genome reproduction
pub struct ReproductionHelper {
    pub cur_innovations: HashMap<Innov, (usize, usize)>, //second data type is a tuple containing the innov, innov+1 if split, and the new node id
    pub innov: usize,
    pub id: usize,
}
impl ReproductionHelper {
    /// Creates a new ReproductionHelper with the given global innov number
    pub fn new(innov: usize, id: usize) -> Self {
        ReproductionHelper { innov, id, cur_innovations: HashMap::new() }
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


    /// Takes an existing genome and mutates it
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
        
        // create new connections, an "add" mutation
        let (bucket_labels, buckets, _, _, _) = Arrays::to_buckets(genome).unwrap(); //unwrap is safe
        let topo = Arrays::toposort(genome).unwrap(); //unwrap is safe
        let layer_nums: Vec<usize> = (0..topo.layers.len()).collect();
        let layers = topo.layers.clone();
        for _ in 0..num_add_mutations { //find a set of two nodes that are currently unconnected
            for _ in 0..6 { //try six times before giving up
                // find a valid node to start at
                let layer = *layer_nums.choose(&mut rng).unwrap();
                let nodes_in_layer = &layers[layer];
                let node = *nodes_in_layer.choose(&mut rng).unwrap(); //start node
                let out_nodes = buckets.get(&layer).unwrap(); //safe unwrap, the nodes our node leads to currently

                // now we want to connect this node to some node in the same layer or after
                let after_layer_nums: Vec<usize> = (layer..layers.len()).collect(); //choose a layer to connect to
                let target_layer = *after_layer_nums.choose(&mut rng).unwrap(); //the layer num we'd like to connect to
                let target_nodes = &layers[target_layer]; //the nodes in the layer we'd like to connect to
                // all the nodes in the layer that this node doesn't connect to
                let not_contained: Vec<usize> = target_nodes.iter().map(|x| (out_nodes.contains(x), *x)).filter(|x| !x.0).map(|x| x.1).collect();
                
                if not_contained.len() == 0 { //we already lead to all of these nodes
                    continue; //try again
                }

                // found a start node and a list of not_contained nodes that we can use as output nodes
                let output_node = *not_contained.choose(&mut rng).unwrap(); //choose an output node

                // ensure this mutation hasn't happened before
                let innov_struct = Innov { in_node: node, out_node: output_node, split: false };
                if self.cur_innovations.contains_key(&innov_struct) { //we've already had this innovation before
                    let innov = *self.cur_innovations.get(&innov_struct).unwrap(); //safe unwrap
                    let gene = ConnectionGene {
                        in_node: node,
                        out_node: output_node,
                        weight: rng.gen_range(-5.0..5.0), //randomized weight
                        enabled: true, //let's just enable by default if mutated into existence
                        innov: innov.0,
                    };
                    genome.connections.push(gene); //push the new mutated connection
                    break;
                } else { //haven't seen this innovation before, 
                    self.cur_innovations.insert(innov_struct, (self.innov, 0)); //remember this innovation
                    let gene = ConnectionGene {
                        in_node: node,
                        out_node: output_node,
                        weight: rng.gen_range(-5.0..5.0), //randomized weight
                        enabled: true, //let's just enable by default if mutated into existence
                        innov: self.innov,
                    };
                    self.innov += 1;
                    genome.connections.push(gene); //push the new mutated connection
                    break;
                }
            }
        }

        // create new nodes, a "split" mutation
        for _ in 0..num_split_mutations { //split any connection
            for _ in 0..6 { //try six times before giving up
                // first select some connection to split
                let connection = genome.connections.choose(&mut rng).unwrap(); //choose an output node
                let innov_struct = Innov { in_node: connection.in_node, out_node: connection.out_node, split: true };
                
                // check if we've split this before
                if self.cur_innovations.contains_key(&innov_struct) {
                    let innov = self.cur_innovations.get(&innov_struct).unwrap(); //safe unwrap

                    // ensure we disable the old connection
                    let connection_mut = genome.connections.choose_mut(&mut rng).unwrap(); //choose an output node, drops old connection
                    connection_mut.enabled = false;
                    let connection = genome.connections.choose(&mut rng).unwrap(); //re-establish the borrow

                    let node_gene = NodeGene {
                        id: innov.1,
                        node_type: 2,
                    };
                    let start_gene = ConnectionGene {
                        in_node: connection.in_node,
                        out_node: innov.1,
                        weight: connection.weight,
                        enabled: true, //let's just enable by default if mutated into existence
                        innov: innov.0,
                    };
                    let end_gene = ConnectionGene {
                        in_node: innov.1,
                        out_node: connection.out_node,
                        weight: 1.0, //set to 1 by default
                        enabled: true, //let's just enable by default if mutated into existence
                        innov: innov.0 + 1,
                    };

                    // push the new genes
                    genome.nodes.push(node_gene);
                    genome.connections.push(start_gene);
                    genome.connections.push(end_gene);
                    break;
                } else { //haven't seen this split before
                    self.cur_innovations.insert(innov_struct, (self.innov, self.id)); //remember this innovation

                    // ensure we disable the old connection
                    let connection_mut = genome.connections.choose_mut(&mut rng).unwrap(); //choose an output node, drops old connection
                    connection_mut.enabled = false;
                    let connection = genome.connections.choose(&mut rng).unwrap(); //re-establish the borrow

                    let node_gene = NodeGene {
                        id: self.id,
                        node_type: 2,
                    };
                    let start_gene = ConnectionGene {
                        in_node: connection.in_node,
                        out_node: self.id,
                        weight: connection.weight,
                        enabled: true,
                        innov: self.innov,
                    };
                    let end_gene = ConnectionGene {
                        in_node: self.id,
                        out_node: connection.out_node,
                        weight: 1.0,
                        enabled: true,
                        innov: self.innov+1,
                    };
                    self.innov += 1;
                    self.id += 1;

                    // push the new genes
                    genome.nodes.push(node_gene);
                    genome.connections.push(start_gene);
                    genome.connections.push(end_gene);
                    break;
                }
            }
        }
    }
}



