/***************************************************/
/**                                               **/
/**   Lucas Wey Hacker   11256952                 **/
/**   Exercicio Programa 1: PageRank              **/
/**   Professor: Saulo Rabello Maciel de Barros   **/
/**   Turma: 01                                   **/
/**                                               **/
/***************************************************/

#include<stdio.h>
#include<stdlib.h>

#define Nmax 500
#define alfa 0.15

void calculaMatrizDeLigacao (int N, float A[][Nmax]){

    int i, j;
    float v[Nmax];

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            v[j] = v[j] + A[i][j];

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            A[i][j] = A[i][j] / v[j];
}

void calculaMatrizGoogle (int N, float A[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            A[i][j] = (1-alfa) * A[i][j] + alfa / N;
}

void subtraiMatrizDaIdentidade (int N, float A[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            if (i == j)
                A[i][j] = A[i][j] -1.0 ;
}

int confereSeTemColunaDeZerosECorrigeSeTiver (int N, float A[][Nmax]){

    int soma, detec;
    int i, j;
    int vecConfereZero[Nmax];
    int vecColunaDeZeros[Nmax];
    float v[Nmax];

    detec = 0;

    for(j = 0; j < N; j = j + 1){
        vecColunaDeZeros[j] = 0;
    }

    for (j = 0; j < N; j = j + 1){
        for (i = 0; i < N; i = i + 1){
            vecConfereZero[i] = 0;
        }
        for (i = 0; i < N; i = i + 1){
            if (A[i][j] == 0){
                vecConfereZero[i] = 1;
            }
        }
        soma = 0;
        for (i = 0; i < N; i = i + 1){
            soma = soma + vecConfereZero[i];
        }
        if (soma == N){
            vecColunaDeZeros[j] = 1;
        }
    }

    for (j = 0; j < N; j = j + 1)
        detec = detec + vecColunaDeZeros[j];

    if (detec == 0)
        return 0;
    else{
        for (i = 0; i < N; i = i + 1)
            for (j = 0; j < N; j = j + 1)
                v[j] = v[j] + A[i][j];

        for (i = 0; i < N; i = i + 1)
            for (j = 0; j < N; j = j + 1)
                if(vecColunaDeZeros[j] == 0)
                    A[i][j] = A[i][j] / v[j];


        for (j = 0; j < N; j = j + 1)
            if (vecColunaDeZeros[j] == 1)
                for (i = 0; i < N; i = i + 1)
                    if (i != j)
                        A[i][j] = 1.0 / (N - 1.0);
        return 1;
    }
}

void geraMatrizAleatoria (int N, float A[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            if (i != j)
                if (rand() % 10 >= 9)
                    A[i][j] = 1.0;
}

int buscaMaiorPivo (int k, int n, float H[][Nmax]){

    int i, posicao;
    float maior;

    maior = H[k][k];
    posicao = k;

    for (i=k; i<n; i=i+1)
        if ( (H[i][k] > maior && maior >= 0.0) || (H[i][k] < maior && maior < 0.0) ){
            maior = H[i][k];
            posicao = i;
        }

    return posicao;
}

void escalonaMatriz (int N, float A[][Nmax]){

    int i, j, k;
    int posicaoDoMaiorPivo;
    float coeficiente, temp;

    for (k = 0; k < (N - 1); k = k + 1){
        posicaoDoMaiorPivo = buscaMaiorPivo(k,N,A);
        if (posicaoDoMaiorPivo != k)
            for (j = 0; j < N; j = j + 1){
                temp = A[k][j];
                A[k][j] = A[posicaoDoMaiorPivo][j];
                A[posicaoDoMaiorPivo][j] = temp;
            }
        for (i = k + 1; i < N; i = i + 1){
            coeficiente = A[i][k] / A[k][k] ;
            for (j = k; j < N; j = j + 1)
                A[i][j]= A[i][j] - coeficiente * A[k][j];
        }
    }
}

void calculaAutovetor (int N, float v[], float A[][Nmax]){

    int k, j;
    float somatoria;

    v[N-1] = 1;

    for (k = (N - 2); k >= 0; k = k - 1){
        somatoria = 0.0;
        for (j = k + 1; j < N; j = j + 1)
            somatoria = somatoria + A[k][j] * v[j];
        v[k]= (-1) * somatoria / A[k][k];
    }
}

void calculaNorma1DeVetor (int N, float v[]){

    int i;
    float parametroNormalizador;

    parametroNormalizador = 0.0;

    for (i = 0; i < N; i = i + 1)
        parametroNormalizador = parametroNormalizador + v[i];

    for (i = 0; i < N; i = i + 1)
        v[i] = v[i] / parametroNormalizador;
}

void imprimeMatriz (int N, float A[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1){
        for (j = 0; j < N; j = j + 1){
            printf(" %f ", A[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void imprimeVetor (int N, float v[]){

    int i;

    for (i = 0; i < N; i = i + 1)
        printf (" %f \n", v[i]);
    printf("\n");
}

int main () {

    int n;               // tamanho da matriz
    int i, j;            // iteradores
    int detec;           // variavel para deteccao se queremos matriz aleatoria
    float M[Nmax][Nmax]; // matriz
    float rank[Nmax];    // vetor com o rank dos sites

    printf ("BEM VINDO AO ALGORITMO DE PAGE RANK \n \n");
    printf ("Entre com o numero de sites da rede: ");
    scanf ("%d", &n);
    printf ("\n");

    while (n > Nmax || n < 0){
        printf("Por favor, entre com um numero de sites positivo e menor que %d \n", Nmax);
        scanf("%d", &n);
    }

    /*Atribui zero para todo termo da matriz M*/
    for (i = 0; i < n; i = i + 1)
        for (j = 0; j < n; j = j + 1)
            M[i][j] = 0.0;

    /*Atribui 0 para todo termo do vetor rank*/
    for (i = 0; i < n; i = i + 1)
        rank[i] = 0.0 ;

    /*Inicializando os termos da matriz M*/
    printf ("Para as proximas perguntas responda 1 para sim e 0 para nao \n \n");
    printf ("Voce deseja gerar uma rede aleatoria para esse conjunto de sites? \n(Caso a resposta seja negativa voce devera entrar manualmente com os dados da rede) \n");
    scanf ("%d", &detec);
    printf ("\n");

    if (detec == 1){
        geraMatrizAleatoria(n, M);
    }
    else {
        for (i = 0; i < n; i = i + 1)
            for (j = 0; j < n; j = j + 1)
                if (j != i){
                    printf ("O site %d eh referido pelo site %d?  ", i+1, j+1);
                    scanf ("%f", &M[i][j]);
                }
        printf ("\n");
    }

    /*Etapas para o calculo do autovetor normalizado de autovalor 1 atraves do metodo de escalonamento*/
    printf("Matriz do grafo: \n \n");
    imprimeMatriz(n, M);

    if(confereSeTemColunaDeZerosECorrigeSeTiver(n, M) == 0){
        calculaMatrizDeLigacao(n, M);
    }

    printf("Matriz de ligacao: \n \n");
    imprimeMatriz(n, M);

    calculaMatrizGoogle(n, M);
    printf("Matriz google: \n \n");
    imprimeMatriz(n, M);

    subtraiMatrizDaIdentidade(n, M);
    printf("Matriz google menos identidade: \n \n");
    imprimeMatriz(n, M);

    escalonaMatriz(n, M);
    printf("Matriz google menos identidade escalonada: \n \n");
    imprimeMatriz(n, M);

    calculaAutovetor(n, rank, M);
    printf("Ranking de importancia nao normalizado: \n \n");
    imprimeVetor(n, rank);

    calculaNorma1DeVetor(n, rank);
    printf("Ranking normalizado: \n \n");
    imprimeVetor(n, rank);

    return 0;
}
