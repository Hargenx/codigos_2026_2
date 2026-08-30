package java_poo.aula05.desafio2.pagamento;

public class PagamentoPix implements FormaPagamento {
    @Override
    public void pagar(double valor) {
        System.out.println("Gerando QR Code PIX...");
        System.out.printf("Pagamento PIX de R$ %.2f realizado com sucesso.%n", valor);
    }
}
