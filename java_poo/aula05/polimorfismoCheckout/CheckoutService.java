package java_poo.aula05.polimorfismoCheckout;

public class CheckoutService {

    public void finalizarCompra(
        double valor,
        FormaPagamento formaPagamento
    ) {

        System.out.println("Finalizando compra...");

        formaPagamento.pagar(valor);

        System.out.println("Pedido criado com sucesso.");
    }
}
