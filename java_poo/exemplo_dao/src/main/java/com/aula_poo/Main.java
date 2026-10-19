package com.aula_poo;

public class Main {
    public static void main(String[] args) {
        try (PessoaDAO dao = new PessoaDAO("alunos")) {
            Pessoa ana = new Pessoa("Ana", 21, 1.67);
            Pessoa bruno = new Pessoa("Bruno", 23, 1.75);

            int idAna = dao.inserirPessoa(ana);
            int idBruno = dao.inserirPessoa(bruno);

            System.out.println("Pessoa consultada: " + dao.buscarPorId(idAna));
            System.out.println("Antes da atualização:");
            dao.listarTodas().forEach(System.out::println);

            boolean atualizou = dao.atualizarPessoa(idAna, "Ana Maria", 22, 1.67);
            boolean excluiu = dao.excluirPessoa(idBruno);
            System.out.println("Atualizou? " + atualizou);
            System.out.println("Excluiu? " + excluiu);

            System.out.println("Após o CRUD:");
            dao.listarTodas().forEach(System.out::println);
        } catch (RuntimeException e) {
            System.err.println("Falha na aplicação: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
