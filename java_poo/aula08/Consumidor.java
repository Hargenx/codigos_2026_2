public class Consumidor implements Runnable {
    private final String nome;
    private final Loja loja;

    public Consumidor(String nome, Loja loja) {
        this.nome = nome;
        this.loja = loja;
    }

    @Override
    public void run() {
        loja.comprar(nome);
    }
}
