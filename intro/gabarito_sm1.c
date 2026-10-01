# include <stdio.h>

int main(void) {

  printf((10 > 5) && (8 < 3) ? "Verdadeiro\n" : "Falso\n");

  double valor = 9.7;
  int inteiro = (int) valor;

  printf("Valor: %d\n", inteiro);

  int a = 5;
  int b = 8;

  if (a < 10 && b > 6){
    printf("Verdadeiro");
  }

  int idade = 20;
  printf("Idade: %d\n", idade);

  int n = 3;

  n = n * 2;

  printf("%d\n", n);

  return 0;
}