package java_poo.aula05.polimorfismoCheckout;

public class PagamentoValePresente
        implements FormaPagamento {

    @Override
    public void pagar(double valor) {

        System.out.printf("Utilizando R$ %.2f do vale-presente.%n", valor);
    }
}
