#include <stdio.h>
#include <stdlib.h>
#include "vector.h"


void test_hashtable() {
    int* buf = malloc(sizeof(int));
    HashTable* ht = hashtable_new(sizeof(Vector*));
    printf("##### statsffffff, %d\n", ht->buckets[100].elem_size);
    int* list = malloc(sizeof(int) * 10);
    list[0] = 18;
    list[1] = 10;
    list[2] = 0;
    list[3] = 34;
    list[4] = 8;
    list[5] = -11;
    list[6] = 49;
    list[7] = 10;
    list[8] = 4;
    list[9] = 5;

    int hash = hashtable_hash_simple(list, 10);
    printf("hash: %d\n", hash);
    printf("caaa\n");
    //Vector* ints = vector_new(sizeof(int));
    Vector* ints = malloc(sizeof(Vector));
    ints->elem_size = sizeof(int);
    ints->elems = (char*)list;
    ints->length = 10;
    ints->capacity = 10;

    *buf = 10;
    printf("baaa\n");


    printf("test: %d\n", vector_in(ints, buf));
    printf("a\n");

    printf("contained: %d\n", hashtable_contains_int_vector(ht, ints));
    printf("ints: %ld ================================\n", (long)ints);
    hashtable_push_int_vector(ht, ints);
    printf("contained: %d\n", hashtable_contains_int_vector(ht, ints));
}


void test_vector() {
    Vector* vec = vector_new(sizeof(int));
    //printf("here2\n");
    int* buf = malloc(sizeof(int));
    *buf = 4;
    //printf("address of int to push: %ld\n", (long)buf);
    //printf("val stored: %d\n", buf[0]);
    vector_push(vec, buf);
    //printf("her32\n");
    *buf = 5;
    vector_push(vec, buf);
    *buf = 10;
    vector_push(vec, buf);
    *buf = -1;
    vector_push(vec, buf);
    //printf("here1\n");
    for (int i = 0; i < vec->length; i++) {
        int* n = vector_index(vec, i);
        printf("(%d) at address: %ld,", *n, (long)n);
    }
    printf("\n");

    *buf = 4;
    printf("%d\n", vector_in(vec, buf));
    *buf = 10;
    printf("%d\n", vector_in(vec, buf));
    *buf = 2;
    printf("%d\n", vector_in(vec, buf));
}


int main() {
    printf("here\n");
    int* a = malloc(sizeof(int));
    *a = 3;
    char* one = (char*)a;
    char* two = &one[1];
    char* three = &one[2];
    char* four = &one[3];
    printf("%d\n", (int)*one);
    printf("%d\n", (int)*two);
    printf("%d\n", (int)*three);
    printf("%d\n", (int)*four);
    printf("%ld\n", (long)one);
    printf("%ld\n", (long)two);
    printf("%ld\n", (long)three);
    printf("%ld\n", (long)four);
    int x = 1;
    char *y = (char*)&x;
    printf("%c\n",*y+48);


    test_vector();
    test_hashtable();


    return 0;
}


