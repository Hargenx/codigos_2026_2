package java_poo.aula05.polimorfismoCheckout;

public class PagamentoBoleto implements FormaPagamento {

    @Override
    public void pagar(double valor) {

        System.out.println("Gerando boleto bancário...");

        System.out.printf(
            "Boleto de R$ %.2f gerado.%n",
            valor
        );
    }
}
