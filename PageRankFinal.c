#include<stdio.h>
#include<stdlib.h>
#include <time.h>

#define Nmax 300
#define alfa 0.15
#define erro 0.00001

#define true 1
#define false 0

void CalculaMatrizDeLigacao (int N, float A[][Nmax]){

    int i, j;
    float aux[Nmax];

    for (i = 0; i < N; i = i + 1)
        aux[i] = 0.0;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            aux[j] = aux[j] + A[i][j]; /*A partir da matriz de adjacencia do grafo calculamos o valor da soma dos elementos de cada coluna (utilizando um vetor auxiliar)*/

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            A[i][j] = A[i][j] / aux[j]; /*E dividindo cada termo da matriz pelo valor armazenado no vetor, obtemos a matriz de Hiperlink (tambem chamada: matriz de ligacao)*/
}

int GravaMatrizEmVetores (int N, float A[][Nmax], float V[], int L[], int C[]){

    int i, j, k;

    k = 0;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            if (A[i][j] != 0){
                V[k] = A[i][j]; /*Os valores dos termos nao nulos da matriz sao armazenados em V*/
                L[k] = i;       /*As posicoes nas linhas desses termos sao armazenadas em L*/
                C[k] = j;       /*As posicoes nas colunas desses termos sao armazenadas em C*/
                k = k + 1;
            }
    return k;                   /* k = numero de elementos dos vetores V, L, C */
}

void CalculaMatrizGoogle (int N, float H[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            H[i][j] = (1 - alfa) * H[i][j] + alfa / N; /* A partir da matriz de Hiperlink H calculamos a matriz google a de acordo com a formula M = (1 − α)M + αSn */
}

void SubtraiMatrizDaIdentidade (int N, float G[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            if (i == j)
                G[i][j] = G[i][j] -1.0 ; /* As entradas da diagonal principal da matriz google sao subtraidas por 1 */
}

int ConfereSeTemColunaDeZerosECorrigeSeTiver (int N, float A[][Nmax]){

    int soma, detec;
    int i, j;
    int vecConfereZero[Nmax];
    int vecColunaDeZeros[Nmax];
    float v[Nmax];

    detec = 0;

    for(j = 0; j < N; j = j + 1)
        vecColunaDeZeros[j] = 0;

    for (j = 0; j < N; j = j + 1){
        for (i = 0; i < N; i = i + 1)
            vecConfereZero[i] = 0;

        for (i = 0; i < N; i = i + 1)
            if (A[i][j] == 0)
                vecConfereZero[i] = 1;

        soma = 0;
        for (i = 0; i < N; i = i + 1)
            soma = soma + vecConfereZero[i];
        if (soma == N)
            vecColunaDeZeros[j] = 1;
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
                        A[i][j] = 1.0 / (N - 1.0); /* Se um site nao apontar para nenhum outro site, supomos entao que o usuario escolhera outro site para navegar aleatoriamente */
        return 1;
    }
}

void GeraMatrizAleatoria (int N, int semente, float A[][Nmax]){

    int i, j;

    srand(semente);
    for (i = 0; i < N; i = i + 1)
        for (j = 0; j < N; j = j + 1)
            if (i != j)
                if (rand() % 10 >= 7) /* De acordo com essa probabilidade atribuimos 1 aleatoriamente aos elementos da matriz */
                    A[i][j] = 1.0;
              /*else
                    A[i][j] = 0.0;*/
}

void GeramMatrizAleatoriaCaciqueTribo (int N, int semente, float A[][Nmax]){

    int i, j;
    int numcacique; /* Numero do cacique no vetor auxiliar */
    float aux[Nmax];

    srand(semente);

    aux[0] = 0.0; /* Suponha sem perda de generalidade que o primeiro site eh um cacique */

    for (i = 1; i < N; i = i + 1)
        if (rand() % 10 >= 3) /* Supondo 70% de um site ser indio*/
            aux[i] = 1.0; /* Indio */
        else
            aux[i] = 0.0; /* Cacique */

    /* Estamos supondo que cada vez que aparece um novo cacique temos entao uma nova tribo */

    for (i = 0; i < N; i = i + 1){
        if (aux[i] == 0)
            for (j = 0; j < i; j = j + 1)
                if (aux[j] == 0 && i != j){
                    A[i][j] = 1.0; /* Conectando o novo cacique aos caciques anteriores */
                    A[j][i] = 1.0;
                }

        else /* aux[i] == 1 */{
            for (j = 0; j < i; j = j + 1)
                if (aux[j] == 0)
                    numcacique = j;

            A[i][numcacique] = 1.0; /* Conectando o indio em questao ao seu cacique*/
            A[numcacique][i] = 1.0;

            if (numcacique != i - 1)
                for (j = numcacique + 1; j < i; j = j + 1){
                    A[i][j] = 1.0; /* Conectando o indio em questao ao seus companheiros indios de tribo */
                    A[j][i] = 1.0;
                }
        }
    }
}

int BuscaMaiorPivo (int k, int n, float A[][Nmax]){

    int i, posicao;
    float maior;

    maior = A[k][k];
    posicao = k;

    for (i = k; i < n; i = i + 1)
        if ((A[i][k] > maior && maior >= 0.0) || (A[i][k] < maior && maior < 0.0)){ /* Procura maior elemento em modulo da coluna da matriz que esta sendo escalonada */
            maior = A[i][k];
            posicao = i;
        }
    return posicao;
}

void Swap (float *a, float *b){

    float temp;

    temp = *a; /* Troca A e B de lugar */
    *a = *b;
    *b = temp;
}

void EscalonaMatriz (int N, float A[][Nmax]){

    int i, j, k;
    int posicaoDoMaiorPivo;
    float coeficiente;

    for (k = 0; k < (N - 1); k = k + 1){
        posicaoDoMaiorPivo = BuscaMaiorPivo(k, N, A);
        if (posicaoDoMaiorPivo != k)
            for (j = 0; j < N; j = j + 1)
                Swap(&A[k][j], &A[posicaoDoMaiorPivo][j]);
        for (i = k + 1; i < N; i = i + 1){
            coeficiente = A[i][k] / A[k][k] ;
            for (j = k; j < N; j = j + 1)
                A[i][j]= A[i][j] - coeficiente * A[k][j]; /* Escalona matriz */
        }
    }
}

void CalculaAutovetor (int N, float v[], float E[][Nmax]){

    int k, j;
    float somatoria;

    v[N-1] = 1;

    for (k = (N - 2); k >= 0; k = k - 1){
        somatoria = 0.0;
        for (j = k + 1; j < N; j = j + 1)
            somatoria = somatoria + E[k][j] * v[j];
        v[k]= (-1) * somatoria / E[k][k];          /* Funcao que calcula o autovetor v a partir da matriz escalonada E */
    }
}

float CalculaC (int N, float G[][Nmax]){

    int i, j;
    float mij, c;

    mij = G[0][0];

    if (1 - (2 * mij) >= 0)
        c = 1 - (2 * mij);
    else /* 1 - (2 * mij) < 0 */
        c = (-1) * (1 - (2 * mij));

    for (j = 0; j < N; j = j + 1){
        for (i = 0; i < N; i = i + 1){
            if (G[i][j] < mij)
                mij = G[i][j];
        }
        if ((1 - (2 * mij) >= 0 && 1 - (2 * mij) > c) || (1 - (2 * mij) < 0 && 1 - (2 * mij) < c))
            c = 1 - (2 * mij);
    }/* Calcula o valor da constante C */

    return c;
}

float CalculaNorma1DeVetor (int N, float v[]){

    int i;
    float parametroNormalizador;

    parametroNormalizador = 0.0;

    for (i = 0; i < N; i = i + 1){
        if (v[i] >= 0.0)
            parametroNormalizador = parametroNormalizador + v[i]; /* A norma 1 eh definida como a soma das entradas em modulo do vetor */
        else /* v[i] < 0.0 */
            parametroNormalizador = parametroNormalizador + (-1) * v[i];
    }

    return parametroNormalizador;
}

void NormalizaVetor (int N, float v[]){

    int i;
    float norma;

    norma = CalculaNorma1DeVetor(N, v);

    for (i = 0; i < N; i = i + 1)
        v[i] = v[i] / norma;      /* Normaliza o vetor de acordo com a norma 1, note que como as entradas do vetor eram todas positivas, a soma das entradas do vetor normalizado sera 1*/
}

void MultiplicaMatrizPorVetorUtilizandoVLC (int Nvec, float y[], float z[] , float V[], int L[], int C[]){

    int i;

    for (i = 0; i < Nvec; i = i + 1)
        z[L[i]] = z[L[i]] + V[i] * y[C[i]]; /* Multiplica Matriz por vetor evitando multiplicacoes por zeros */
}

void ImprimeMatriz (int N, float A[][Nmax]){

    int i, j;

    for (i = 0; i < N; i = i + 1){
        for (j = 0; j < N; j = j + 1){
            printf(" %f ", A[i][j]);
        }
        printf("\n");
    }
}

void ImprimeVetor (int N, float v[]){

    int i;

    for (i = 0; i < N; i = i + 1)
        printf (" %f \n", v[i]);
    printf("\n");
}

void ImprimeVetorINT (int N, int v[]){

    int i;

    for (i = 0; i < N; i = i + 1)
        printf (" %d \n", v[i]);
    printf("\n");
}

void CalculaAutovetorMetodoIterativo (int N, int Nvec, float c, float vec[], float V[], int L[], int C[]){

    int i, j;
    float z[Nmax], vAntigo[Nmax];
    float soma;

    j = 1;

    do{
        soma = 0.0;

        for (i = 0; i < N; i = i + 1)
            z[i] = 0.0;

        for (i = 0; i < N; i = i + 1)
            vAntigo[i] = vec[i];

        MultiplicaMatrizPorVetorUtilizandoVLC(Nvec, vec, z, V, L, C);

        for (i = 0; i < N; i = i + 1)
            vec[i] = (1 - alfa) * z[i] + alfa / N;

        for (i = 0; i < N; i = i + 1)
            z[i] = vec[i] - vAntigo[i];

        soma = CalculaNorma1DeVetor(N, z);

        printf ("x(%d) = \n", j);
        ImprimeVetor(N, vec);
        j = j + 1;

    } while ((c / (1.0 - c))*soma >= erro );
}

void OrdenaVetorEImprime (int N, float v[]){

    int i, j, houveTrocas;
    float aux[Nmax];

    for (i = 0; i < N; i = i + 1)
        aux[i] = i + 1;

    houveTrocas = true;

    for (j = N - 1; j > 0 && houveTrocas == true; j = j - 1){
        houveTrocas = false;
        for (i = 0; i < j; i = i + 1)
            if (v[i] < v[i + 1]){
                Swap (&v[i], &v[i + 1]); /* Algoritmo do Bubble sort para ordenar o vetor */
                Swap (&aux[i], &aux[i + 1]);
                houveTrocas = true;
            }
    }

    for (i = 0; i < N; i = i + 1)
        printf (" O %d-esimo site eh o numero %.0f com ranking  = %f \n", i + 1, aux[i], v[i]);
    printf("\n");
}

int main () {

    int n;                       /* tamanho da matriz M */
    int numeroElementosNaoNulos; /* numero de termos dos vetores V, L, C */
    int i, j;                    /* iteradores */
    int detecMatrizAleatoria;    /* variavel para deteccao se queremos matriz aleatoria */
    int detecCaciqueTribo;       /* variavel para deteccao se queremos rede de sites que segue uma arquitetura do tipo Cacique-Tribo */
    int num;                     /* numero para gerar as matrizes aleatorias */
    float M[Nmax][Nmax];         /* matriz principal */
    float V[Nmax*Nmax - Nmax];   /* vetor dos valores */
    int L[Nmax*Nmax - Nmax];     /* vetor do valor das linhas */
    int C[Nmax*Nmax - Nmax];     /* vetor com os valores das colunas */
    float rank[Nmax];            /* vetor com o rank dos sites */
    float c;                     /* valor da constante para o calculo do erro no metodo iterativo */

    printf (" BEM VINDO AO ALGORITMO DE PAGE RANK \n");
    printf ("\n Entre com o numero de sites da rede: ");
    scanf ("%d", &n);

    while (n > Nmax || n < 0){
        printf("\n Por favor, entre com um numero de sites positivo e menor que %d: ", Nmax);
        scanf("%d", &n);
    }

    /*Atribui zero para todo termo da matriz M*/
    for (i = 0; i < n; i = i + 1)
        for (j = 0; j < n; j = j + 1)
            M[i][j] = 0.0;

    /*Atribui 0 para todo termo do vetor rank*/
    for (i = 0; i < n; i = i + 1)
        rank[i] = 0.0;

    /*Inicializando os termos da matriz M*/
    printf ("\n Para as proximas perguntas: \n Se sua resposta for SIM, digite 1 \n Se sua resposta for NAO, digite 0 \n");
    printf ("\n Trata-se de uma rede de sites seguindo a arquitetura do tipo Cacique-Tribo ? ");
    scanf ("%d", &detecCaciqueTribo);
    printf ("\n Voce deseja gerar uma rede aleatoria para esse conjunto de sites? ");
    scanf ("%d", &detecMatrizAleatoria);

    if (detecCaciqueTribo == true){
        if (detecMatrizAleatoria == true) {
            printf("\n Digite um numero para nos servir de inpiracao para gerar numeros aleatorios: ");
            scanf("%d", &num);
            GeramMatrizAleatoriaCaciqueTribo (n, num, M);
        }
        else {
            for (i = 0; i < n; i = i + 1)
                for (j = 0; j < i; j = j + 1){
                    printf ("\n O site %d eh referido pelo site %d?  ", i+1, j+1);
                    scanf ("%f", &M[i][j]);
                    M[j][i] = M[i][j]; /*propriedade da arquitetura Cacique-Tribo*/
                }
        }
    }
    else {
        if (detecMatrizAleatoria == true){
            printf("\n Digite um numero para nos servir de inpiracao para gerar numeros aleatorios: ");
            scanf("%d", &num);
            GeraMatrizAleatoria(n, num, M);
        }
        else {
            for (i = 0; i < n; i = i + 1)
                for (j = 0; j < n; j = j + 1)
                    if (j != i){
                        printf ("\n O site %d eh referido pelo site %d?  ", i+1, j+1);
                        scanf ("%f", &M[i][j]);
                    }
                    /*else (i = j){
                        M[i][j] = 0.0;  pois estamos supondo que nenhum site possui um link para ele mesmo
                    }*/
        }
    }

    /*Etapas para o calculo do autovetor normalizado de autovalor 1*/
    printf("\n Matriz de adjacencia do grafo: \n");
    ImprimeMatriz(n, M);

    if(ConfereSeTemColunaDeZerosECorrigeSeTiver(n, M) == 0){
        CalculaMatrizDeLigacao(n, M);
    }

    printf("\n Matriz de ligacao: \n");
    ImprimeMatriz(n, M);

    numeroElementosNaoNulos = GravaMatrizEmVetores(n, M, V, L, C);
    printf("\n Vetor V: \n");
    ImprimeVetor(numeroElementosNaoNulos, V);
    printf("\n Vetor L: \n");
    ImprimeVetorINT(numeroElementosNaoNulos, L);
    printf("\n Vetor C: \n");
    ImprimeVetorINT(numeroElementosNaoNulos, C);

    CalculaMatrizGoogle(n, M);
    printf("\n Matriz google com alfa = %f : \n", alfa);
    ImprimeMatriz(n, M);

    c = CalculaC(n, M);
    printf("\n O valor de C = %f \n", c);

    printf("\n METODO ESCALONAMENTO: \n");

    SubtraiMatrizDaIdentidade(n, M);
    printf("\n Matriz google menos identidade: \n");
    ImprimeMatriz(n, M);

    EscalonaMatriz(n, M);
    printf("\n Matriz google menos identidade escalonada: \n");
    ImprimeMatriz(n, M);

    CalculaAutovetor(n, rank, M);
    printf("\n Ranking dos sites nao normalizado: \n");
    ImprimeVetor(n, rank);

    NormalizaVetor(n, rank);
    printf("\n Ranking dos sites normalizado: \n");
    ImprimeVetor(n, rank);

    printf("\n METODO ITERATIVO: \n");

    /*Atribui 1/n para todo termo do vetor rank*/
    for (i = 0; i < n; i = i + 1)
        rank[i] = 1.0 / n;

    printf (" x(0) = \n");
        ImprimeVetor(n, rank);

    CalculaAutovetorMetodoIterativo(n, numeroElementosNaoNulos, c, rank, V, L, C);

    printf("\n Ranking dos sites normalizado para erro = %f : \n", erro);
    ImprimeVetor(n, rank);

    OrdenaVetorEImprime(n, rank);

    return 0;
}
