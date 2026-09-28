class Transferencia implements Runnable {

    private final Pessoa origem;
    private final Pessoa destino;

    public Transferencia(Pessoa origem, Pessoa destino) {
        this.origem = origem;
        this.destino = destino;
    }

    @Override
    public void run() {

        if (origem.getSaldo() > 0) {
            origem.retirar(1);
            destino.receber(1);
        }
    }
}