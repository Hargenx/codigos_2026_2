class TransferenciaOrdenada implements Runnable {

    private final Pessoa origem;
    private final Pessoa destino;

    public TransferenciaOrdenada(
            Pessoa origem,
            Pessoa destino) {

        this.origem = origem;
        this.destino = destino;
    }

    @Override
    public void run() {

        Pessoa primeiro;
        Pessoa segundo;

        if (origem.getId() < destino.getId()) {
            primeiro = origem;
            segundo = destino;
        } else {
            primeiro = destino;
            segundo = origem;
        }

        synchronized (primeiro) {

            synchronized (segundo) {

                if (origem.getSaldo() > 0) {

                    origem.retirar(1);
                    destino.receber(1);
                }
            }
        }
    }
}