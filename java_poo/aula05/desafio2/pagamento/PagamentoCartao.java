package java_poo.aula05.desafio2.pagamento;

public class PagamentoCartao implements FormaPagamento {
    private String numeroCartao;

    public PagamentoCartao(String numeroCartao) {
        this.numeroCartao = numeroCartao;
    }

    @Override
    public void pagar(double valor) {
        System.out.println("Enviando transação para a operadora...");
        System.out.printf("Pagamento de R$ %.2f aprovado no cartão %s.%n", valor, mascararCartao());
    }

    private String mascararCartao() {
        return "**** **** **** " + numeroCartao.substring(numeroCartao.length() - 4);
    }
}
