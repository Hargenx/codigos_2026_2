package com.aula_poo_dao;

/*public class Main {
    public static void main(String[] args) {
        try (PessoaDAO dao = new PessoaDAO("Alunos")) {
            // Instancias da classe
            Pessoa pessoa1 = new Pessoa(1, "Rafael", 42, (float) 1.88);
            Pessoa pessoa2 = new Pessoa(2, "Fox", 30, (float) 1.65);
            Pessoa pessoa3 = new Pessoa(3, "Ikit Claw", 45, (float) 1.42);
            Pessoa pessoa4 = new Pessoa(4, "Kroq-Gar", 8500, (float) 1.42);
            // Insere pessoa - C
            dao.inserirPessoa(pessoa1);
            dao.inserirPessoa(pessoa2);
            dao.inserirPessoa(pessoa3);
            dao.inserirPessoa(pessoa4);
            // Exibe todas as pessoas
            System.out.println("Todas as pessoas:");
            dao.obterTodasPessoas().forEach(System.out::println);

            // Alterar uma pessoa - U
            dao.alterarPessoa(1, "Raphael", null, (float) 1.82);
            System.out.println("Pessoa após alteração:");
            System.out.println(dao.obterPessoaPorId(1));
            // Apagar uma pessoa - D
            dao.apagarPessoa(3);
            System.out.println("Pessoa após exclusão:");
            System.out.println(dao.obterPessoaPorId(3));
            // Apagar uma pessoa - D
            dao.apagarPessoa(3);
            pessoa2 = dao.obterPessoaPorId(3);
            System.out.println(pessoa2);
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println(e.getMessage());
        }
    }
}*/


public class Main {
    public static void main(String[] args) {
        try (PessoaDAO2 dao = new PessoaDAO2("alunos")) {
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