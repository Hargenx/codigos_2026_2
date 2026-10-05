package java_poo.aula09;

import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ExecutorService;

public class Consultar {
    static double consultar(String empresa, int espera, double valor)
            throws InterruptedException {

        System.out.println("Consultando " + empresa + "...");
        Thread.sleep(espera); // simula chamada HTTP
        return valor;
    }

    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(3);

        Future<Double> correios = executor.submit(
                () -> consultar("Correios", 1800, 32.90));

        Future<Double> a = executor.submit(
                () -> consultar("Transportadora A", 1200, 27.50));

        Future<Double> b = executor.submit(
                () -> consultar("Transportadora B", 2200, 29.90));

        double melhor = Math.min(
                correios.get(), Math.min(a.get(), b.get()));

        System.out.println("Melhor valor: " + melhor);

        try (var executor2 = Executors.newVirtualThreadPerTaskExecutor()) {
            Future<Double> frete = executor.submit(
                    () -> consultar("Transportadora", 1500, 27.50));

            System.out.println(frete.get());
        }

        executor.shutdown();
    }

}
