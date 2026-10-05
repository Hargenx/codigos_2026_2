package java_poo.aula09;

public class Correios {
    public static double consultar(String empresa, int prazo, double valor) {
        System.out.println("Consultando " + empresa);
        try {
            Thread.sleep(prazo);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return valor;
    }

    public Correios() {
    }
    
}
