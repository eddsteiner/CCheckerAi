#ifndef VECTOR_H_
#define VECTOR_H_


typedef struct Vector {
    int capacity;
    int length;
    int elem_size;
    char* elems;
} Vector;


Vector* vector_new(int elem_size);
void vector_push(Vector* vec, void* val);
void* vector_index(Vector* vec, int index);
void vector_update(Vector* vec, int index, void* val);
int vector_in(Vector* vec, void* val);


#endif //VECTOR_H_

