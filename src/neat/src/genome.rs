use std::collections::{HashMap, HashSet};



pub struct NodeGene {
    pub id: usize,
    pub node_type: u8,
}


pub struct ConnectionGene {
    pub in_node: usize,
    pub out_node: usize,
    pub weight: f32,
    pub enabled: bool,
    pub innov: usize,
}


pub struct Genome {
    pub nodes: Vec<NodeGene>,
    pub connections: Vec<ConnectionGene>,
    pub input_ids: HashSet<usize>, //makes life easier
    pub output_ids: HashSet<usize>,
}
impl Genome {
    pub fn with_capacities(nodes: usize, connections: usize) -> Self {
        Genome {
            nodes: Vec::with_capacity(nodes),
            connections: Vec::with_capacity(connections),
            input_ids: HashSet::new(),
            output_ids: HashSet::new(),
        }
    }
}


pub struct Arrays {
    multiplier: Vec<f32>,
    source: Vec<f32>,
    dest: Vec<f32>,
    output: Vec<f32>,
    mult_threads: Vec<usize>,
    output_threads: Vec<usize>,
}
impl Arrays {
    pub fn with_capacities(mult: usize, src: usize, dest: usize, output: usize, mult_th: usize, output_th: usize) -> Self {
        Arrays {
            multiplier: Vec::with_capacity(mult),
            source: Vec::with_capacity(src),
            dest: Vec::with_capacity(dest),
            output: Vec::with_capacity(output),
            mult_threads: Vec::with_capacity(mult_th),
            output_threads: Vec::with_capacity(output_th)
        }
    }

    pub fn from_genome(genome: &Genome) -> Option<Self> {
        Some(Arrays::from_topo(Arrays::toposort(genome)?)) //first run topo, then convert topo to Arrays
    }


    pub fn from_topo(topo: Vec<Vec<usize>>) -> Self {
        todo!()
    }

    pub fn toposort(genome: &Genome) -> Option<Vec<Vec<usize>>> {
        
        // populate the buckets with all the enabled connections (excluding output connections)
        let mut bucket_labels: HashSet<usize> = HashSet::new();
        let mut buckets: HashMap<usize, HashSet<usize>> = HashMap::new();
        let mut cur_layer: HashSet<usize> = HashSet::new(); //for toposort
        println!("Genome connections: {:?}", genome.connections.len());
        for i in 0..genome.connections.len() {
            let cur_connect = &genome.connections[i];
            //println!("Enabled and contained? {:?}, {:?}", cur_connect.enabled, genome.output_ids.contains(&cur_connect.out_node));
            //if cur_connect.enabled && !genome.output_ids.contains(&cur_connect.out_node) { //valid connection
            if cur_connect.enabled { //valid connection
                if genome.input_ids.contains(&cur_connect.in_node) { //start building the first layer for the toposort
                    cur_layer.insert(cur_connect.in_node);
                }

                // push to a bucket, create if necessary
                if !bucket_labels.contains(&cur_connect.in_node) { //we don't yet have a bucket for this in_node, create one
                    bucket_labels.insert(cur_connect.in_node);
                    buckets.insert(cur_connect.in_node, HashSet::new());
                }
                buckets.get_mut(&cur_connect.in_node)?.insert(cur_connect.out_node); //push the out_node to the bucket for in_node
            } 
        }

        // now that we have the buckets, begin toposort
        let mut past_layers: HashMap<usize, Vec<(u32, HashSet<usize>)>> = HashMap::new(); //<hash, <(layer_number, <layer_ids>)>>
        past_layers.insert(292, vec![(0, genome.input_ids.clone())]); //push the input ids as layer 0
        let mut layer_number = 0; //will get stored with every layer
        while cur_layer.len() > 0 { //while a frontier still exists for the next layer
            layer_number += 1;
            
            // build the new layer
            let mut new_layer: HashSet<usize> = HashSet::new();
            for input in &cur_layer {
                println!("input: {}", input);
                let extend_ids = buckets[&input].iter().filter(|x| !genome.output_ids.contains(x)); //remove output ids
                new_layer.extend(extend_ids); //because hash we don't have to worry about repeat output ids
            }

            // finished building the new layer so hash and see if we've seen this before
            let hash = cur_layer.iter().fold(0, |a, x| (a + x) * 3 % 293); //very simple hash
            if past_layers.contains_key(&hash) { //we've seen this hash before
                let repeat = past_layers[&hash].iter().any(|h| h.1 == cur_layer);
                if repeat { //yup, this layer has been seen before, CYCLIC
                    return None;
                }
                // NOTE: we can unwrap here because we know the hash exists
                past_layers.get_mut(&hash).unwrap().push((layer_number, cur_layer.clone())); //not cyclic and haven't seen before, remember it
                cur_layer = new_layer; //replace
            } else { //never seen this hash before, so add it and continue as usual
                past_layers.insert(hash, vec![(layer_number, new_layer.clone())]); //remember this layer
            }
        }

        // out of the loop, now grab all layers from past_layers and sort them into a list
        let mut numbered_layers: Vec<(u32, HashSet<usize>)> = past_layers.into_iter().flat_map(|hash| hash.1).collect();
        numbered_layers.sort_unstable_by_key(|x| x.0);
        let topo = numbered_layers.into_iter().map(|x| x.1.into_iter().collect()).collect(); //remove numbers and convert hashset to vector
        Some(topo)
    }
}










