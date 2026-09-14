package java_poo.aula06.exemplo02;

import java.io.IOException;

public class ExemploThrows {
    void umMetodo(int num) throws IOException, ArithmeticException{
        if (num == 1){
            throw new IOException("Cai no IOException");
        }else{
            throw new ArithmeticException("Cai no ArithmeticException");
        }
    }
}
