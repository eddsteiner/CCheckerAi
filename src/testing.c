#include <stdio.h>
#include <stdlib.h>
#include "vector.h"

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


    return 0;
}


