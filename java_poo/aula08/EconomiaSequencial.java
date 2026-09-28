import java.util.ArrayList;
import java.util.List;
import java.util.Random;

class Pessoa {

    private final int id;
    private int saldo;

    public Pessoa(int id, int saldo) {
        this.id = id;
        this.saldo = saldo;
    }

    public int getId() {
        return id;
    }

    public int getSaldo() {
        return saldo;
    }

    public void retirar(int valor) {
        saldo -= valor;
    }

    public void receber(int valor) {
        saldo += valor;
    }

    @Override
    public String toString() {
        return "Pessoa " + id + ": R$ " + saldo;
    }
}

public class EconomiaSequencial {

    private static final Random random = new Random();

    public static void main(String[] args) {

        List<Pessoa> pessoas = new ArrayList<>();

        for (int i = 0; i < 20; i++) {
            pessoas.add(new Pessoa(i, 100));
        }

        for (int rodada = 0; rodada < 10_000; rodada++) {

            Pessoa origem =
                    pessoas.get(random.nextInt(pessoas.size()));

            Pessoa destino;

            do {
                destino =
                        pessoas.get(random.nextInt(pessoas.size()));
            } while (origem == destino);

            if (origem.getSaldo() > 0) {
                origem.retirar(1);
                destino.receber(1);
            }
        }

        mostrarResultado(pessoas);
    }

    private static void mostrarResultado(List<Pessoa> pessoas) {

        int total = 0;

        for (Pessoa pessoa : pessoas) {
            System.out.println(pessoa);
            total += pessoa.getSaldo();
        }

        System.out.println("---------Sequencial-------");
        System.out.println("Dinheiro total: R$ " + total);
    }
}