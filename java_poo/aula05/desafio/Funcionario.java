package java_poo.aula05.desafio;

abstract class Funcionario {
    protected String nome;

    public Funcionario(String nome) {
        this.nome = nome;
    }

    // Método abstrato para representar a atividade de trabalho do funcionário
    public abstract void servico();

    // Método abstrato para calcular o salário do funcionário
    public abstract double calcularSalario();
}
