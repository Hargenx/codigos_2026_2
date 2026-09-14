package java_poo.aula06.exemplo03;

public class Main {

    public static void main(String[] args) {

        CheckoutService checkout = new CheckoutService();

        try {

            checkout.finalizarCompra(
                3,
                2500
            );

        } catch (EstoqueInsuficienteException e) {

            System.out.println(
                "Não foi possível concluir a compra: "
                + e.getMessage()
            );

        } catch (PagamentoRecusadoException e) {

            System.out.println(
                "Problema no pagamento: "
                + e.getMessage()
            );

        } catch (IllegalArgumentException e) {

            System.out.println(
                "Dados inválidos: "
                + e.getMessage()
            );

        } finally {

            System.out.println(
                "Processamento do checkout encerrado."
            );
        }
    }
}