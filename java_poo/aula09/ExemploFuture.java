package java_poo.aula09;

import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ExecutorService;

public class ExemploFuture {
    ExecutorService executor = Executors.newFixedThreadPool(3);

Future<Double> correios = executor.submit(
    () -> consultar("Correios", 1800, 32.90));

Future<Double> a = executor.submit(
    () -> consultar("Transportadora A", 1200, 27.50));

Future<Double> b = executor.submit(
    () -> consultar("Transportadora B", 2200, 29.90));

double melhor = Math.min(
    correios.get(), Math.min(a.get(), b.get()));

executor.shutdown();

}
