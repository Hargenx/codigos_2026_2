package java_poo.aula05.abstracaoArmazem;

public class DocumentoService {
    private Armazenamento armazenamento;

    public DocumentoService(Armazenamento armazenamento) {
        this.armazenamento = armazenamento;
    }

    public void enviarDocumento(String nome, byte[] arquivo) {
        System.out.println("Validando documento...");
        if (arquivo.length == 0) {
            System.out.println("Arquivo inválido.");
            return;
        }

        String caminho = armazenamento.salvar(nome, arquivo);
        System.out.println("Documento registrado:");
        System.out.println(caminho);
    }
}