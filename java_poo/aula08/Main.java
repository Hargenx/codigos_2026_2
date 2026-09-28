import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main {
    public static void main(String[] args) {
        Loja loja = new Loja();
        ExecutorService executor = Executors.newFixedThreadPool(4);

        for (int i = 1; i <= 10; i++) {
            executor.submit(
                    new Consumidor("Agente " + i, loja));

        }
        executor.shutdown();
    }
}
