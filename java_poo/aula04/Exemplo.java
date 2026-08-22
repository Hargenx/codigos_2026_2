package java_poo.aula04;

public class Exemplo {
    public static void main(String[] args) {
        MinhaClasse obj = new MinhaClasse();
        // Acessando atributos
        System.out.println("Atributo default: " + obj.defaultAtributo);
        System.out.println("Atributo protected: " + obj.protectedAtributo);
        System.out.println("Atributo public: " + obj.publicAtributo);
        // A linha abaixo geraria erro, pois privateAtributo não é acessível fora da classe
        // System.out.println("Atributo private: " + obj.privateAtributo);
        // Chamando métodos
        obj.defaultMetodo();
        obj.protectedMetodo();
        obj.publicMetodo();
        // A linha abaixo geraria erro, pois privateMetodo não é acessível fora da classe
        // obj.privateMetodo();
        obj.chamarPrivate(); // Método que internamente chama o método private
        // Criando uma subclasse e demonstrando o acesso aos membros herdados
        SubClasse sub = new SubClasse();
        sub.acessarAtributos();
    }

}
