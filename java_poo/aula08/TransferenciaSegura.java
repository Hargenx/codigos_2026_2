class TransferenciaSegura implements Runnable {

    private final Pessoa origem;
    private final Pessoa destino;

    private static final Object lock = new Object();

    public TransferenciaSegura(
            Pessoa origem,
            Pessoa destino) {

        this.origem = origem;
        this.destino = destino;
    }

    @Override
    public void run() {

        synchronized (lock) {

            if (origem.getSaldo() > 0) {
                origem.retirar(1);
                destino.receber(1);
            }
        }
    }
}