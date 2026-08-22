package java_poo.aula04;

public class SubClasse extends MinhaClasse {
    void acessarAtributos() {
        System.out.println("\nNa SubClasse:");
        // Pode acessar atributos default, protected e public da classe pai
        System.out.println("Atributo default: " + defaultAtributo);
        System.out.println("Atributo protected: " + protectedAtributo);
        System.out.println("Atributo public: " + publicAtributo);
        // A linha abaixo geraria erro, pois privateAtributo não é herdado
        // System.out.println("Atributo private: " + privateAtributo);
        // Chamando métodos herdados
        defaultMetodo();
        protectedMetodo();
        publicMetodo();
        // A linha abaixo geraria erro, pois privateMetodo não é acessível
        // privateMetodo();
    }

}
