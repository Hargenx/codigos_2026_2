package java_poo.aula05.desafio;

public class Terceirizado extends Funcionario {
    private double valorHora;
    private int horasTrabalhadas;

    public Terceirizado(String nome, double valorHora, int horasTrabalhadas) {
        super(nome);
        this.valorHora = valorHora;
        this.horasTrabalhadas = horasTrabalhadas;
    }

    @Override
    public void servico() {
        System.out.println("Terceirizado " + nome + " está realizando tarefas terceirizadas.");
    }

    @Override
    public double calcularSalario() {
        return valorHora * horasTrabalhadas;
    }
    
}
