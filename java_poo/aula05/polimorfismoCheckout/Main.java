package java_poo.aula05.polimorfismoCheckout;

public class Main {

    public static void main(String[] args) {

        CheckoutService checkout =
            new CheckoutService();

        FormaPagamento pagamento1 =
            new PagamentoPix();

        checkout.finalizarCompra(
            199.90,
            pagamento1
        );

        System.out.println("--------------------");

        FormaPagamento pagamento2 =
            new PagamentoCartao("1234567812345678");

        checkout.finalizarCompra(
            499.90,
            pagamento2
        );

        System.out.println("--------------------");

        FormaPagamento pagamento3 =
            new PagamentoBoleto();

        checkout.finalizarCompra(
            89.90,
            pagamento3
        );
    }
}
