package java_poo.aula06.exemplo03;

public class EstoqueService {

    private int estoqueDisponivel = 5;

    public void reservar(int quantidade) throws EstoqueInsuficienteException {

        if (quantidade > estoqueDisponivel) {
            throw new EstoqueInsuficienteException(
                "Estoque insuficiente. Disponível: " + estoqueDisponivel
            );
        }

        estoqueDisponivel -= quantidade;

        System.out.println("Estoque reservado com sucesso.");
    }
}