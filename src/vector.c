#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>


typedef struct Vector {
    int capacity;
    int length;
    int elem_size;
    char* elems;
} Vector;


typedef struct HashMap {
    void** buckets;
} HashMap;


// Create a new vector with default new size of 2
static Vector* vector_new(int elem_size) {
    Vector* vec = malloc(sizeof(Vector));
    vec->capacity = 2;
    vec->length = 0;
    vec->elem_size = elem_size;
    vec->elems = malloc(elem_size * 2);
    return vec;
}


// Simple method to push onto a Vector
static void vector_push(Vector* vec, void* val) {
    char* bval = (char*)val;
    if (vec->length < vec->capacity - 1) { //simply append the new value
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    } else { //need to reallocate, then push
        char* new_elems = malloc(vec->elem_size * vec->capacity * 2);
        memcpy(new_elems, vec->elems, vec->elem_size * vec->capacity);
        free(vec->elems);
        vec->elems = new_elems;

        // now push after reallocating
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    }
}


// Index a vector
static void* vector_index(Vector* vec, int index) {
    return &vec[index * vec->elem_size];
}


// Update a vector
static void vector_update(Vector* vec, int index, void* val) {
    char* cur = vector_index(vec, index);
    for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
        cur[i] = ((char*)val)[i];
    }
}


// Returns the index if the value is in the vector, -1 otherwise
static int vector_in(Vector* vec, void* val) {
    char* bval = (char*)val;
    char* index;
    int in;
    for (int i = 0; i < vec->length; i++) { //for each element
        index = (char*)vector_index(vec, i);
        in = 1;
        for (int j = 0; j < vec->elem_size; j++) { //for each byte of an element
            if (bval[j] != index[j]) {
                in = 0;
                break;
            }
        }
        if (in == 1) {
            return i;
        }
    }
    return -1;
}
















