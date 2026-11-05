package com.fintech.pagamento;

import com.fintech.pagamento.dao.PagamentoDAO;
import com.fintech.pagamento.model.*;
import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        try (PagamentoDAO dao = new PagamentoDAO("financeiro.db")) {
            Pagamento[] novos = {
                new PagamentoPix(100.0, "chave@exemplo.com", "QR-EXEMPLO"),
                new PagamentoCartao(250.0, "**** **** **** 1234", "VISA", 3),
                new PagamentoBoleto(180.0, "34191-EXEMPLO", LocalDate.now().plusDays(7))
            };
            for (Pagamento pagamento : novos) {
                dao.salvar(pagamento);
                System.out.println("Salvo: " + pagamento);
            }
            System.out.println("\n--- Todos os pagamentos (polimorfismo) ---");
            dao.listarTodos().forEach(System.out::println);
            System.out.println("\n--- Busca por código ---");
            System.out.println(dao.buscarPorCodigo(novos[0].getCodigoTransacao()));
        } catch (Exception e) {
            System.err.println("Erro: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
