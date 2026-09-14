package java_poo.aula06.exemplo03;

public class CheckoutService {

    private EstoqueService estoqueService;
    private PagamentoService pagamentoService;

    public CheckoutService() {
        estoqueService = new EstoqueService();
        pagamentoService = new PagamentoService();
    }

    public void finalizarCompra(
            int quantidade,
            double valor
    ) throws EstoqueInsuficienteException,
             PagamentoRecusadoException {

        if (quantidade <= 0) {
            throw new IllegalArgumentException(
                "A quantidade deve ser maior que zero."
            );
        }

        estoqueService.reservar(quantidade);

        pagamentoService.pagar(valor);

        System.out.println("Pedido confirmado!");
    }
}