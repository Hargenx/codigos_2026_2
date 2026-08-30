package java_poo.aula05.abstracaoArmazem;

public interface Armazenamento {
    String salvar(String nomeArquivo, byte[] conteudo);
    void remover(String caminho);
}
