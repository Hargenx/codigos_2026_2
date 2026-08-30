package java_poo.aula05.abstracaoArmazem;

public class Main {
    public static void main(String[] args) {
        byte[] contrato = "Contrato exemplo".getBytes();

        Armazenamento armazenamento = new ArmazenamentoCloud();
        DocumentoService documentos = new DocumentoService(armazenamento);

        documentos.enviarDocumento("contrato.pdf", contrato);
    }
}