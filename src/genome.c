#include <stdlib.h>
#include <stdint.h>
#include "genome.h"


void dealloc_genome_internals(Genome* genome) {
    free(genome->nodes);
    free(genome->connections);
}


