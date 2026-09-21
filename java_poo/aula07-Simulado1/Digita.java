import java.util.Scanner;

public class Digita {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite um número inteiro: ");
        int numero = scanner.nextInt();
        System.out.println("Você digitou: " + numero);
        System.out.println("O dobro do número digitado é: " + (numero * 2));
        System.out.print("Digite o seu nome: ");
        String nome = scanner.next();
        System.out.println("Olá, " + nome + "!");
        scanner.close();
    }
}