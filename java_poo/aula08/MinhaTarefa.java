class MinhaTarefa implements Runnable {
    @Override
    public void run() {
        System.out.println(
            "Dentro de run(): " + Thread.currentThread().getState()
        );

        try {
            Thread.sleep(2000); // TIMED_WAITING durante a pausa
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
