package java_poo.aula05.desafio;

public class Main {
    public static void main(String[] args) {
        // Array de Funcionario contendo diferentes tipos de funcionários
        Funcionario[] Funcionarios = new Funcionario[4];
        Funcionarios[0] = new Desenvolvedor("Raphael", 40_000.0, 10, 50.0);
        Funcionarios[1] = new Gerente("Gilson", 50_000.0, 1500.0);
        Funcionarios[2] = new Estagiario("Sara", 3_000.0);
        Funcionarios[3] = new Terceirizado("Raquel", 25.0, 160);
        // Iteração polimórfica: cada objeto "sabe" como executar seus próprios métodos
        for (Funcionario emp : Funcionarios) {
            emp.servico();
            System.out.println("Salário: R$ " + emp.calcularSalario());
            System.out.println("---------------------------------");
        }
    }

}
