#ifndef GENOME_H_
#define GENOME_H_


#define PY_SSIZE_T_CLEAN
#include <python3.11/Python.h>
#include <stdint.h>


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
    long innov; //shared across genomes, combination of in and out
} ConnectionGene;


// Contains a genome, consisting of NodeGenes and ConnectionGenes.
typedef struct Genome {
    NodeGene* nodes;
    ConnectionGene* connections;
    int node_count;
    int connection_count;
} Genome;


typedef struct Arrays {
    double* multiplier;
    double* source;
    double* dest;
    double* output;
    long* mult_threads;
    long* output_threads;

    long multiplier_len;
    long source_len;
    long dest_len;
    long output_len;
    long mult_threads_len;
    long output_threads_len;
} Arrays;


//typedef struct Topo {
//    int layers;
//    int* layer_sizes;
//    int* ids;
//} Topo;


// A nice way to initialize Arrays
static void initialize_arrays(Arrays* arrays) {
    if (arrays != NULL) {
        arrays->multiplier = NULL;
        arrays->source = NULL;
        arrays->dest = NULL;
        arrays->output = NULL;
        arrays->mult_threads = NULL;
        arrays->output_threads = NULL;

        arrays->multiplier_len = 0;
        arrays->source_len = 0;
        arrays->dest_len = 0;
        arrays->output_len = 0;
        arrays->mult_threads_len = 0;
        arrays->output_threads_len = 0;
    }
}


// A nice way to copy an Arrays struct
static void copy_arrays(Arrays* dest, Arrays* source) {
    printf("made it here\n");
    if (dest == NULL) {
        printf("dest is null\n");
    }
    if (source == NULL) {
        printf("source is null\n");
    }
    dest->multiplier = (double*)malloc(sizeof(double) * source->multiplier_len);
    dest->source = (double*)malloc(sizeof(double) * source->source_len);
    dest->dest = (double*)malloc(sizeof(double) * source->dest_len);
    dest->output = (double*)malloc(sizeof(double) * source->output_len);
    dest->mult_threads = (long*)malloc(sizeof(long) * source->mult_threads_len);
    dest->output_threads = (long*)malloc(sizeof(long) * source->output_threads_len);
    printf("first block\n");

    memcpy(dest->multiplier, source->multiplier, sizeof(double) * source->multiplier_len);
    memcpy(dest->source, source->source, sizeof(double) * source->source_len);
    memcpy(dest->dest, source->dest, sizeof(double) * source->dest_len);
    memcpy(dest->output, source->output, sizeof(double) * source->output_len);
    memcpy(dest->mult_threads, source->mult_threads, sizeof(long) * source->mult_threads_len);
    memcpy(dest->output_threads, source->output_threads, sizeof(long) * source->output_threads_len);

    dest->multiplier_len = source->multiplier_len;
    dest->source_len = source->source_len;
    dest->dest_len = source->dest_len;
    dest->output_len = source->output_len;
    dest->mult_threads_len = source->mult_threads_len;
    dest->output_threads_len = source->output_threads_len;
    printf("no issues here\n");
}


/// Deallocate a genome
void dealloc_genome_internals(Genome* genome);
void dealloc_array_internals(Arrays* arrays);


#endif //GENOME_H_

