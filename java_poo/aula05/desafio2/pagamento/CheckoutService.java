package java_poo.aula05.desafio2.pagamento;

public class CheckoutService {
    public void finalizarCompra(double valor, FormaPagamento formaPagamento) {
        System.out.println("Finalizando compra...");

        formaPagamento.pagar(valor);

        System.out.println("Compra finalizada.");
        System.out.println("--------------------------------");
    }
}