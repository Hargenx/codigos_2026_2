package java_poo.aula05;

public interface Armazenamento {

    String salvar(String nomeArquivo, byte[] conteudo);

    void remover(String caminho);
}