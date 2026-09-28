public class ExemploEstados {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new MinhaTarefa(), "worker");

        System.out.println(thread.getState()); // NEW
        thread.start();

        Thread.sleep(100);                    // dá tempo para entrar em sleep()
        System.out.println(thread.getState()); // TIMED_WAITING

        thread.join();
        System.out.println(thread.getState()); // TERMINATED
    }
}
