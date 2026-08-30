package java_poo.aula05.desafio;

class Estagiario extends Funcionario {
    private double estipendio;

    public Estagiario(String nome, double estipendio) {
        super(nome);
        this.estipendio = estipendio;
    }

    @Override
    public void servico() {
        System.out.println("Estagiário " + nome + " está auxiliando nas tarefas.");
    }

    @Override
    public double calcularSalario() {
        // Estagiário recebe um valor fixo (bolsa)
        return estipendio;
    }
}
