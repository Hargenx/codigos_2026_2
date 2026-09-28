public class Loja {
    private int estoque = 5;

    public synchronized void comprar(String consumidor) {
        if (estoque > 0) {
            estoque--;
            System.out.println(consumidor + " encontrou produto");
            System.out.println(
                consumidor + " comprou. Estoque: " + estoque
            );
        }
    }
}
