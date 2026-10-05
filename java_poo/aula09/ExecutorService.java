package java_poo.aula09;

import java.util.concurrent.Executors;
import java.util.concurrent.Future;

final class ExecutorService {
    ExecutorService executor = Executors.newFixedThreadPool(4);

    Future<Double> futuro = executor.submit(() -> consultarFrete());

    Double valor = futuro.get();
    executor.shutdown();

}
