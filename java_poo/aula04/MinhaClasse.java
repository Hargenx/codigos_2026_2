package java_poo.aula04;

public class MinhaClasse {
    /*
     * Acesso default (package-private):
     * visível apenas para classes do mesmo pacote
     */
    int defaultAtributo = 1;
    /*
     * Acesso protected:
     * visível para classes do mesmo pacote e subclasses
     */
    protected int protectedAtributo = 2;
    // Acesso public: visível para todas as classes
    public int publicAtributo = 3;
    // Acesso private: visível apenas dentro desta classe
    private int privateAtributo = 4;

    // Método com acesso default
    void defaultMetodo() {
        System.out.println("Método default");
    }

    // Método com acesso protected
    protected void protectedMetodo() {
        System.out.println("Método protected");
    }

    // Método com acesso public
    public void publicMetodo() {
        System.out.println("Método public: " + this.privateAtributo);
    }

    // Método com acesso private
    private void privateMetodo() {
        System.out.println("Método private");
    }
    
    // Método público que permite chamar o método private internamente
    public void chamarPrivate() {
        privateMetodo();
    }

}
