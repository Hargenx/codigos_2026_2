package com.fintech.pagamento.dao;

import com.fintech.pagamento.model.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Types;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class PagamentoDAO implements AutoCloseable {
    private final Connection conexao;

    public PagamentoDAO(String arquivoBanco) throws SQLException {
        try {
            Path caminho = Path.of("db", arquivoBanco).toAbsolutePath();
            Files.createDirectories(caminho.getParent());
            conexao = DriverManager.getConnection("jdbc:sqlite:" + caminho);
        } catch (IOException e) {
            throw new SQLException("Falha ao criar pasta do banco.", e);
        }
        try {
            criarTabela();
        } catch (SQLException e) {
            try {
                conexao.close();
            } catch (SQLException fechamento) {
                e.addSuppressed(fechamento);
            }
            throw e;
        }
    }

    private void criarTabela() throws SQLException {
        String sql = """
                CREATE TABLE IF NOT EXISTS pagamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_transacao TEXT NOT NULL UNIQUE,
                    tipo_pagamento TEXT NOT NULL CHECK(tipo_pagamento IN ('PIX','CARTAO','BOLETO')),
                    valor REAL NOT NULL CHECK(valor > 0),
                    data_hora TEXT NOT NULL,
                    status TEXT NOT NULL,
                    chave_pix TEXT, qr_code TEXT,
                    numero_cartao_mascarado TEXT, bandeira TEXT, parcelas INTEGER,
                    codigo_barras TEXT, data_vencimento TEXT
                )
                """;
        try (Statement st = conexao.createStatement()) {
            st.execute(sql);
        }
    }

    public boolean salvar(Pagamento pagamento) throws SQLException {
        String sql = """
                INSERT INTO pagamentos (
                    codigo_transacao, tipo_pagamento, valor, data_hora, status,
                    chave_pix, qr_code, numero_cartao_mascarado, bandeira,
                    parcelas, codigo_barras, data_vencimento
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;
        try (PreparedStatement ps = conexao.prepareStatement(sql)) {
            ps.setString(1, pagamento.getCodigoTransacao());
            ps.setString(2, pagamento.getTipo());
            ps.setDouble(3, pagamento.getValor());
            ps.setString(4, pagamento.getDataHora().toString());
            ps.setString(5, pagamento.getStatus());
            ps.setString(6, pagamento instanceof PagamentoPix pix ? pix.getChavePix() : null);
            ps.setString(7, pagamento instanceof PagamentoPix pix ? pix.getQrCode() : null);
            ps.setString(8, pagamento instanceof PagamentoCartao cartao ? cartao.getNumeroCartaoMascarado() : null);
            ps.setString(9, pagamento instanceof PagamentoCartao cartao ? cartao.getBandeira() : null);
            if (pagamento instanceof PagamentoCartao cartao)
                ps.setInt(10, cartao.getParcelas());
            else
                ps.setNull(10, Types.INTEGER);
            ps.setString(11, pagamento instanceof PagamentoBoleto boleto ? boleto.getCodigoBarras() : null);
            ps.setString(12,
                    pagamento instanceof PagamentoBoleto boleto ? boleto.getDataVencimento().toString() : null);
            if (ps.executeUpdate() != 1)
                return false;
        }
        try (Statement st = conexao.createStatement();
                ResultSet rs = st.executeQuery("SELECT last_insert_rowid()")) {
            rs.next();
            pagamento.setId(rs.getInt(1));
        }
        return true;
    }

    public List<Pagamento> listarTodos() throws SQLException {
        List<Pagamento> lista = new ArrayList<>();
        try (Statement st = conexao.createStatement();
                ResultSet rs = st.executeQuery("SELECT * FROM pagamentos ORDER BY id")) {
            while (rs.next())
                lista.add(converter(rs));
        }
        return lista;
    }

    public Pagamento buscarPorCodigo(String codigo) throws SQLException {
        try (PreparedStatement ps = conexao.prepareStatement(
                "SELECT * FROM pagamentos WHERE codigo_transacao = ?")) {
            ps.setString(1, codigo);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? converter(rs) : null;
            }
        }
    }

    private Pagamento converter(ResultSet rs) throws SQLException {
        int id = rs.getInt("id");
        String codigo = rs.getString("codigo_transacao");
        double valor = rs.getDouble("valor");
        LocalDateTime data = LocalDateTime.parse(rs.getString("data_hora"));
        String status = rs.getString("status");
        return switch (rs.getString("tipo_pagamento")) {
            case "PIX" -> new PagamentoPix(id, codigo, valor, data, status,
                    rs.getString("chave_pix"), rs.getString("qr_code"));
            case "CARTAO" -> new PagamentoCartao(id, codigo, valor, data, status,
                    rs.getString("numero_cartao_mascarado"), rs.getString("bandeira"), rs.getInt("parcelas"));
            case "BOLETO" -> new PagamentoBoleto(id, codigo, valor, data, status,
                    rs.getString("codigo_barras"), LocalDate.parse(rs.getString("data_vencimento")));
            default -> throw new SQLException("Tipo de pagamento desconhecido no banco.");
        };
    }

    @Override
    public void close() throws SQLException {
        conexao.close();
    }
}
