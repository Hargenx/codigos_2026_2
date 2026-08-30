package java_poo.aula05.desafio2.pagamento;

public class Main {
    public static void main(String[] args) {

        CheckoutService checkout = new CheckoutService();

        FormaPagamento pix = new PagamentoPix();

        FormaPagamento cartao = new PagamentoCartao("1234567812345678");

        FormaPagamento boleto = new PagamentoBoleto();

        checkout.finalizarCompra(150.00, pix);
        checkout.finalizarCompra(350.00, cartao);
        checkout.finalizarCompra(500.00, boleto);
    }

}
