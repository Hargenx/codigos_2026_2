package java_poo.aula09;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;



public class ExemploBlockingQueue {
    BlockingQueue<String> fila = new ArrayBlockingQueue<>(10);

    // Produtor
    executor.submit(() -> {
        fila.put("pedido-123");
        return null;
    });

    // Consumidor
    executor.submit(() -> {
        String pedido = fila.take();
        processar(pedido);
        return null;
    });

}
