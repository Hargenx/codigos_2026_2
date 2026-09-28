import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class EconomiaExecutor {

    private static final Random random = new Random();

    public static void main(String[] args)
            throws InterruptedException {

        List<Pessoa> pessoas = new ArrayList<>();

        for (int i = 0; i < 20; i++) {
            pessoas.add(new Pessoa(i, 100));
        }

        ExecutorService executor =
                Executors.newFixedThreadPool(4);

        for (int i = 0; i < 10_000; i++) {

            Pessoa origem =
                    pessoas.get(random.nextInt(pessoas.size()));

            Pessoa destino;

            do {
                destino =
                        pessoas.get(random.nextInt(pessoas.size()));
            } while (origem == destino);

            executor.submit(
                    new TransferenciaSegura(
                            origem,
                            destino
                    )
            );
        }

        executor.shutdown();

        executor.awaitTermination(
                1,
                TimeUnit.MINUTES
        );

        mostrarResultado(pessoas);
    }

    private static void mostrarResultado(List<Pessoa> pessoas) {

        int total = 0;

        for (Pessoa pessoa : pessoas) {

            System.out.println(pessoa);

            total += pessoa.getSaldo();
        }

        System.out.println("---------Executor-------");
        System.out.println(
                "Dinheiro total: R$ " + total
        );
    }
}