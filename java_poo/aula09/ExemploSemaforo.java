package java_poo.aula09;

import java.util.concurrent.Semaphore;

class ExemploSemaforo {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                acessarApi();
            }).start();
        }
    }

    private static void acessarApi() {
        Semaphore limite = new Semaphore(3);

        try {
            limite.acquire();

            try {
                consultarApi();
            } finally {
                limite.release();
            }

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private static void consultarApi() {
        System.out.println("Consultando API: " + Thread.currentThread().getName());
        try {
            Thread.sleep(2000); // Simula o tempo de consulta à API
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

