use std::collections::{HashMap, HashSet};



#[derive(Clone, Debug)]
pub struct NodeGene {
    pub id: usize,
    pub node_type: u8,
}


#[derive(Clone, Debug)]
pub struct ConnectionGene {
    pub in_node: usize,
    pub out_node: usize,
    pub weight: f32,
    pub enabled: bool,
    pub innov: usize,
}


#[derive(Clone, Debug)]
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


#[derive(Clone, Debug)]
pub struct TopoStruct<'a> {
    pub layers: Vec<Vec<usize>>, //toposorted layers
    //nodes: Vec<&'a NodeGene>, //only enabled nodes
    pub connections: Vec<&'a ConnectionGene>, //only enabled connections
    pub connections_map: HashMap<usize, Vec<&'a ConnectionGene>>, //maps an to its output connections
}


#[derive(Clone, Debug)]
pub struct Arrays {
    pub multiplier: Vec<f32>,
    pub source: Vec<usize>,
    pub dest: Vec<usize>,
    pub output: Vec<f32>,
    pub mult_threads: Vec<usize>,
    pub output_threads: Vec<usize>,
}
impl Arrays {
    //pub fn with_capacities(mult: usize, src: usize, dest: usize, output: usize, mult_th: usize, output_th: usize) -> Self {
    //    Arrays {
    //        multiplier: Vec::with_capacity(mult),
    //        source: Vec::with_capacity(src),
    //        dest: Vec::with_capacity(dest),
    //        output: Vec::with_capacity(output),
    //        mult_threads: Vec::with_capacity(mult_th),
    //        output_threads: Vec::with_capacity(output_th)
    //    }
    //}

    pub fn from_genome(genome: &Genome) -> Option<Self> {
        Some(Arrays::from_topo(genome, Arrays::toposort(genome)?)) //first run topo, then convert topo to Arrays
    }


    pub fn from_topo(genome: &Genome, topo: TopoStruct) -> Self {
        let mut arrs = Arrays {
            multiplier: vec![0.0; topo.connections.len()],
            source: vec![0; topo.connections.len()],
            dest: vec![0; topo.connections.len()],
            output: vec![0.0; genome.nodes.len()],
            mult_threads: vec![0; topo.layers.len()],
            output_threads: vec![0; topo.layers.len()],
        };

        // reorder ids to simplify later processes
        let mut new_map: HashMap<usize, (usize, Vec<&ConnectionGene>)> = HashMap::new(); //maps an id to a new id and output connections
        let mut new_topo = topo.layers.clone();
        new_topo.push(genome.output_ids.iter().map(|x| *x).collect());
        let topo_nums: Vec<(usize, usize)> = new_topo.into_iter().flatten().enumerate().collect(); //new, old
        for (i, e) in topo_nums {
            match topo.connections_map.get(&e) {
                None => {
                    new_map.insert(e, (i, Vec::new()));
                },
                Some(connections) => {
                    new_map.insert(e, (i, connections.clone()));
                },

            }
        }

        // load values into the arrays
        let mut arrs_offset = 0;
        for i in 0..topo.layers.len() {
            let layer = &topo.layers[i];
            let connections: Vec<&ConnectionGene> = layer.iter().map(|x| topo.connections_map[x].clone()).flatten().collect(); //ids to connections
            for j in 0..connections.len() { //push data to multiplier, source, and dest
                arrs.multiplier[arrs_offset + j] = connections[j].weight;
                arrs.source[arrs_offset + j] = new_map[&connections[j].in_node].0;
                arrs.dest[arrs_offset + j] = new_map[&connections[j].out_node].0;
            }
            arrs_offset += connections.len();

            arrs.mult_threads[i] = connections.len();
            if i == topo.layers.len()-1 { //on the last layer, set to the number of outputs
                arrs.output_threads[i] = genome.output_ids.len();
            } else {
                arrs.output_threads[i] = topo.layers[i+1].len();
            }
        }

        arrs.output[0] = 1.0; //set the bias input
        arrs
    }

    /// Turns a genome into layers, or None if genome encodes for a cyclic neural net
    pub fn toposort(genome: &Genome) -> Option<TopoStruct> {
        
        // populate the buckets with all the enabled connections (excluding output connections)
        let mut bucket_labels: HashSet<usize> = HashSet::new();
        let mut buckets: HashMap<usize, HashSet<usize>> = HashMap::new();
        let mut buckets_genes: HashMap<usize, Vec<&ConnectionGene>> = HashMap::new(); //for arrays conversion
        let mut active_connections: Vec<&ConnectionGene> = Vec::new(); //for arrays conversion
        //let mut active_nodes: Vec<&NodeGene> = Vec::new(); //for arrays conversion
        let mut cur_layer: HashSet<usize> = HashSet::new(); //for toposort
        for i in 0..genome.connections.len() {
            let cur_connect = &genome.connections[i];
            if cur_connect.enabled { //valid connection
                active_connections.push(cur_connect);
                if genome.input_ids.contains(&cur_connect.in_node) { //start building the first layer for the toposort
                    cur_layer.insert(cur_connect.in_node);
                }

                // push to a bucket, create if necessary
                if !bucket_labels.contains(&cur_connect.in_node) { //we don't yet have a bucket for this in_node, create one
                    bucket_labels.insert(cur_connect.in_node);
                    buckets.insert(cur_connect.in_node, HashSet::new());
                    buckets_genes.insert(cur_connect.in_node, Vec::new());
                }
                buckets.get_mut(&cur_connect.in_node)?.insert(cur_connect.out_node); //push the out_node to the bucket for in_node
                buckets_genes.get_mut(&cur_connect.in_node)?.push(&cur_connect); //push the connection to the bucket for in_node
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
                let extend_ids = buckets[&input].iter().filter(|x| !genome.output_ids.contains(x)); //remove output ids
                new_layer.extend(extend_ids); //because hash we don't have to worry about repeat output ids
            }

            // don't push an empty set
            if new_layer.len() == 0 {
                break;
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
            } else { //never seen this hash before, so add it and continue as usual
                past_layers.insert(hash, vec![(layer_number, new_layer.clone())]); //remember this layer
                println!("past_layers: {:?}", past_layers);
            }
            cur_layer = new_layer; //replace
        }

        // out of the loop, now grab all layers from past_layers and sort them into a list
        let mut numbered_layers: Vec<(u32, HashSet<usize>)> = past_layers.into_iter().flat_map(|hash| hash.1).collect();
        numbered_layers.sort_unstable_by_key(|x| x.0);
        let layers = numbered_layers.into_iter().map(|x| x.1.into_iter().collect()).collect(); //remove numbers and convert hashset to vector

        let topo = TopoStruct { layers: layers, connections: active_connections, connections_map: buckets_genes };
        Some(topo)
    }
}










