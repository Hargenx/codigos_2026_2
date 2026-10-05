package java_poo.aula09;

import java.util.concurrent.Semaphore;

class ClienteFrete {
    private final Semaphore limite = new Semaphore(3);

    public void consultar(String pedido) {
        try {
            limite.acquire();
            try {
                System.out.println(pedido + " consultando API...");
                Thread.sleep(1500); // simula rede
                System.out.println(pedido + " finalizado");
            } finally {
                limite.release();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}


