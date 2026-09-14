package java_poo.aula06.exemplo03;

public class PagamentoService {

    public void pagar(double valor)
            throws PagamentoRecusadoException {

        if (valor > 3000) {
            throw new PagamentoRecusadoException(
                "Pagamento recusado pela operadora."
            );
        }

        System.out.println("Pagamento de R$ " + valor + " aprovado.");
    }
}