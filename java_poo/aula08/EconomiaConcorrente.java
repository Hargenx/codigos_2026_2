import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class EconomiaConcorrente {

    private static final Random random = new Random();

    public static void main(String[] args)
            throws InterruptedException {

        List<Pessoa> pessoas = new ArrayList<>();

        for (int i = 0; i < 20; i++) {
            pessoas.add(new Pessoa(i, 100));
        }

        List<Thread> threads = new ArrayList<>();

        for (int i = 0; i < 10_000; i++) {

            Pessoa origem =
                    pessoas.get(random.nextInt(pessoas.size()));

            Pessoa destino;

            do {
                destino =
                        pessoas.get(random.nextInt(pessoas.size()));
            } while (origem == destino);

            Thread thread = new Thread(
                    new Transferencia(origem, destino)
            );

            threads.add(thread);
            thread.start();
        }

        for (Thread thread : threads) {
            thread.join();
        }

        mostrarResultado(pessoas);
    }

    private static void mostrarResultado(List<Pessoa> pessoas) {

        int total = 0;

        for (Pessoa pessoa : pessoas) {
            System.out.println(pessoa);
            total += pessoa.getSaldo();
        }

        System.out.println("---------Concorrente-------");
        System.out.println("Dinheiro total: R$ " + total);
    }
}