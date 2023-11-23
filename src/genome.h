#ifndef GENOME_H_
#define GENOME_H_


// Contains one node gene in a genome.
typedef struct NodeGene {
    int id; //unique
    uint8_t type; //0 = input, 1 = output, 2 = hidden, 3 = end/delimiter
} NodeGene;


// Contains one connection gene in a genome.
typedef struct ConnectionGene {
    int in;
    int out;
    double weight;
    uint8_t enabled; //0 = disabled, 1 = enabled, 2 = end/delimiter
    int innov; //shared across genomes, combination of in and out
} ConnectionGene;


// Contains a genome, consisting of NodeGenes and ConnectionGenes.
typedef struct Genome {
    NodeGene* nodes;
    ConnectionGene* connections;
    int node_count;
    int connection_count;
} Genome;


/// Deallocate a genome
void dealloc_genome_internals(Genome* genome);


#endif //GENOME_H_


