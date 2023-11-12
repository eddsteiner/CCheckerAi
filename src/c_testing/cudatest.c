#include <stdlib.h>
#include <stdio.h>
#include <string.h>

extern void maxmul(float *A, float* B, float *C, int size);

int main() {
    printf("hi\n");

    //a := []C.float{-1,2,4,0,5,3,6,2,1}
	//b := []C.float{3,0,2,3,4,5,4,7,2}
	//var c []C.float = make([]C.float, 9)
	//Maxmul(a,b,c,3)
	//fmt.Println(c)

    float* a = malloc(9 * sizeof(float));
    float* b = malloc(9 * sizeof(float));
    float* c = malloc(9 * sizeof(float));

    memcpy(a, (float[]){-1, 2, 4, 0, 5, 3, 6, 2, 1}, 9 * sizeof(a[0]));
    memcpy(b, (float[]){3, 0, 2, 3, 4, 5, 4, 7, 2}, 9 * sizeof(b[0]));
    maxmul(a, b, c, 3);

    for (int i = 0; i < 9; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");


    return 0;
}


