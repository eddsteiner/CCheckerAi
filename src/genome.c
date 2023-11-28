#include <stdlib.h>
#include <stdint.h>
#include "genome.h"


void dealloc_genome_internals(Genome* genome) {
    free(genome->nodes);
    free(genome->connections);
}


void dealloc_array_internals(Arrays* arrays) {
    free(arrays->multiplier);
    free(arrays->source);
    free(arrays->dest);
    free(arrays->output);
    free(arrays->mult_threads);
    free(arrays->output_threads);
}

