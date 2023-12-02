#ifndef VECTOR_H_
#define VECTOR_H_


typedef struct Vector {
    int capacity;
    int length;
    int elem_size;
    char* elems;
} Vector;


typedef struct HashTable {
    Vector buckets[1000];
} HashTable;


Vector* vector_new(int elem_size);
void vector_push(Vector* vec, void* val);
void* vector_index(Vector* vec, int index);
void vector_update(Vector* vec, int index, void* val);
int vector_in(Vector* vec, void* val);

HashTable* hashtable_new(int elem_size);
int hashtable_hash_simple(int* nums, int size);
void hashtable_push(HashTable* hashtable, void* elem, int hash);
Vector* hashtable_match(HashTable* hashtable, int hash);
int hashtable_contains_int_vector(HashTable* hashtable, Vector* ints);
void hashtable_push_int_vector(HashTable* hashtable, Vector* ints);


#endif //VECTOR_H_

