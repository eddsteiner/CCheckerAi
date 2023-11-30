#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "vector.h"


#define HASHTABLE_SIZE 293


// Create a new vector with default new size of 2
Vector* vector_new(int elem_size) {
    Vector* vec = malloc(sizeof(Vector));
    vec->capacity = 2;
    vec->length = 0;
    vec->elem_size = elem_size;
    vec->elems = malloc(elem_size * 2);
    return vec;
}


// Simple method to push onto a Vector
void vector_push(Vector* vec, void* val) {
    char* bval = (char*)val;
    if (vec->length < vec->capacity) { //simply append the new value
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    } else { //need to reallocate, then push
        char* new_elems = malloc(vec->elem_size * vec->capacity * 2);
        memcpy(new_elems, vec->elems, vec->elem_size * vec->capacity);
        free(vec->elems);
        vec->elems = new_elems;
        vec->capacity = vec->capacity * 2;

        // now push after reallocating
        for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
            vec->elems[vec->length * vec->elem_size + i] = bval[i];
        }
        vec->length = vec->length + 1;
    }
}


// Index a vector
void* vector_index(Vector* vec, int index) {
    return &vec->elems[index * vec->elem_size];
}


// Update a vector
void vector_update(Vector* vec, int index, void* val) {
    char* cur = vector_index(vec, index);
    for (int i = 0; i < vec->elem_size; i++) { //push all bytes for the new value
        cur[i] = ((char*)val)[i];
    }
}


// Returns the index if the value is in the vector, -1 otherwise
int vector_in(Vector* vec, void* val) {
    char* bval = (char*)val;
    char* index;
    int in;
    for (int i = 0; i < vec->length; i++) { //for each element
        //printf("a\n");
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
        //printf("b\n");
    }
    return -1;
}


// Create a new hashmap
HashTable* hashtable_new(int elem_size) {
    HashTable* hashtable = malloc(sizeof(HashTable));
    for (int i = 0; i < HASHTABLE_SIZE; i++) { //initialize all vectors
        hashtable->buckets[i] = *vector_new(elem_size);
        printf("##### stats, %d\n", hashtable->buckets[i].elem_size);
    }
    return hashtable;
}


// Simple hash meant for arrays of integers
int hashtable_hash_simple(int* nums, int size) {
    long sum = 0;
    for (int i = 0; i < size; i++) {
        sum = (3 * (sum + nums[i])) % HASHTABLE_SIZE;
    }
    return (int)sum;
}


// Push a new element onto the hashmap based on the provided hash
void hashtable_push(HashTable* hashtable, void* elem, int hash) {
    vector_push(&hashtable->buckets[hash], elem);
    printf("aaaaaaaaa: %ld\n", (long)vector_index(&hashtable->buckets[hash], 0)); //somehow not the same???
    printf("##### stats, %d\n", hashtable->buckets[hash].elem_size);
}


// Retrieve the vectors correlating to the given hash
Vector* hashtable_match(HashTable* hashtable, int hash) {
    return &hashtable->buckets[hash];
    printf("##### stats, %d\n", hashtable->buckets[hash].elem_size);
}


// Simple verification for int vectors
int hashtable_contains_int_vector(HashTable* hashtable, Vector* ints) {
    printf("##### statsn, %d\n", ints->elem_size);
    int* arr = (int*)ints->elems;
    int size = ints->length;
    Vector* cur;
    int hash = hashtable_hash_simple(arr, size); //generate hash for the new vector
    Vector* matches = hashtable_match(hashtable, hash); //get the existing values
    printf("matches length: %d\n", matches->length);
    printf("##### statsaa, %d\n", matches->elem_size);
    for (int i = 0; i < matches->length; i++) { //iterate through all lists
        //printf("before!\n");
        //cur = (Vector*)(matches->elems[i]);
        cur = vector_index(matches, i);
        printf("cur: %ld\n", (long)cur);
        //printf("after!\n");
        if (size != cur->length) { //sizes do not match, cannot be the same list
            printf("sizes didnt match, %d %d\n", size, cur->length);
            continue;
        }
        printf("thing elemsize: %d\n", cur->elem_size);
        int pass = 1;
        for (int j = 0; j < size; j++) { //check every element
            printf("thing size: %d\n", cur->length);
            printf("thing elemsize: %d\n", cur->elem_size);
            int x = *(int*)vector_index(cur, j);
            printf("aaaaa\n");
            int y = arr[j];
            int z = x == y;
            //if (arr[j] != (*(int*)vector_index(cur, j))) { //no match, continue to next list
            if (!z) { //no match, continue to next list
                printf("bbbbb\n");
                pass = 0;
                break;
            }
            printf("bbbbb\n");
        }
        if (pass == 1) { //we found no differences between the two lists, pass
            return 1;
        }
    }
    return 0; //was never able to finish on a success, so no pass
}


// Simple push for an int vector
void hashtable_push_int_vector(HashTable* hashtable, Vector* ints) {
    int* arr = (int*)ints->elems;
    int size = ints->length;

    int contained = hashtable_contains_int_vector(hashtable, ints);
    if (contained != 0) {
        return;
    }

    // push if not in the table yet
    int hash = hashtable_hash_simple(arr, size);
    printf("hash: %d\n", hash);
    printf("bouta_push_ints: %ld\n", (long)ints);
    hashtable_push(hashtable, ints, hash);
}



