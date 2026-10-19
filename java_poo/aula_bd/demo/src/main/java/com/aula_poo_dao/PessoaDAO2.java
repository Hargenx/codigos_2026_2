package com.aula_poo_dao;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class PessoaDAO2 implements AutoCloseable {
    private final Connection conexao;

    public PessoaDAO2(String nomeBanco) {
        try {
            Path caminho = Path.of("db", nomeBanco + ".db").toAbsolutePath();
            Files.createDirectories(caminho.getParent());
            conexao = DriverManager.getConnection("jdbc:sqlite:" + caminho);
            criarTabela();
        } catch (IOException | SQLException e) {
            throw new IllegalStateException("Falha ao abrir o banco", e);
        }
    }

    private void criarTabela() {
        String sql = """
                CREATE TABLE IF NOT EXISTS pessoas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL CHECK (idade >= 0),
                    altura REAL NOT NULL CHECK (altura > 0)
                )
                """;
        try (Statement stmt = conexao.createStatement()) {
            stmt.executeUpdate(sql);
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao criar a tabela", e);
        }
    }

    public int inserirPessoa(Pessoa pessoa) {
        String sql = "INSERT INTO pessoas (nome, idade, altura) VALUES (?, ?, ?)";
        try (PreparedStatement ps = conexao.prepareStatement(
                sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, pessoa.getNome());
            ps.setInt(2, pessoa.getIdade());
            ps.setDouble(3, pessoa.getAltura());
            ps.executeUpdate();
            try (ResultSet chaves = ps.getGeneratedKeys()) {
                if (chaves.next()) {
                    int id = chaves.getInt(1);
                    pessoa.setId(id);
                    return id;
                }
            }
            throw new IllegalStateException("ID da pessoa não retornado");
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao inserir pessoa", e);
        }
    }

    public Pessoa buscarPorId(int id) {
        String sql = "SELECT id, nome, idade, altura FROM pessoas WHERE id = ?";
        try (PreparedStatement ps = conexao.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? mapearPessoa(rs) : null;
            }
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao buscar pessoa", e);
        }
    }

    public List<Pessoa> listarTodas() {
        List<Pessoa> pessoas = new ArrayList<>();
        String sql = "SELECT id, nome, idade, altura FROM pessoas ORDER BY id";
        try (PreparedStatement ps = conexao.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                pessoas.add(mapearPessoa(rs));
            }
            return pessoas;
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao listar pessoas", e);
        }
    }

    private Pessoa mapearPessoa(ResultSet rs) throws SQLException {
        return new Pessoa(rs.getInt("id"), rs.getString("nome"),
                rs.getInt("idade"), rs.getDouble("altura"));
    }

    public boolean atualizarPessoa(int id, String nome, int idade, double altura) {
        String sql = "UPDATE pessoas SET nome = ?, idade = ?, "
                + "altura = ? WHERE id = ?";
        try (PreparedStatement ps = conexao.prepareStatement(sql)) {
            ps.setString(1, nome);
            ps.setInt(2, idade);
            ps.setDouble(3, altura);
            ps.setInt(4, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao atualizar pessoa", e);
        }
    }

    public boolean excluirPessoa(int id) {
        String sql = "DELETE FROM pessoas WHERE id = ?";
        try (PreparedStatement ps = conexao.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao excluir pessoa", e);
        }
    }

    @Override
    public void close() {
        try {
            conexao.close();
        } catch (SQLException e) {
            throw new IllegalStateException("Falha ao fechar a conexão", e);
        }
    }
}
