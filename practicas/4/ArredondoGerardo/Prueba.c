#include <stdio.h>

void main(){
    int i, k, j; 
    int arr[2][3][5]={2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60};
    int a1[10];
    char letra[15]="Algoritmos en C"; 
    for(i = 0; i<2; i++){ 
        for(j=0; j<3; j++){
            for(k=0; k<5; k++){
                printf("Arreglo [%d][%d][%d]: %d\n", i,j,k,arr[i][j][k]); 
            }
        }
    }

    for(i=0; i<10;i++){
        a1[i] = i+3;
    }
    
    printf("\n\n");

    printf("\n\n");
}
