package com.aula_poo;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class PessoaDAOTest {
    private String nomeBanco;
    private Path arquivoBanco;

    @BeforeEach
    void prepararBanco() {
        nomeBanco = "teste-" + UUID.randomUUID();
        arquivoBanco = Path.of("db", nomeBanco + ".db").toAbsolutePath();
    }

    @AfterEach
    void apagarBancoDeTeste() throws IOException {
        Files.deleteIfExists(arquivoBanco);
    }

    @Test
    void deveFazerCrudEPersistirEntreConexoes() {
        int id;
        try (PessoaDAO dao = new PessoaDAO(nomeBanco)) {
            Pessoa pessoa = new Pessoa("Ana", 21, 1.67);
            id = dao.inserirPessoa(pessoa);
            assertTrue(id > 0);
            assertEquals(id, pessoa.getId());
            assertEquals("Ana", dao.buscarPorId(id).getNome());
            assertEquals(1, dao.listarTodas().size());
            assertTrue(dao.atualizarPessoa(id, "Ana Maria", 22, 1.68));
            assertEquals("Ana Maria", dao.buscarPorId(id).getNome());
        }
        // Abre o mesmo arquivo novamente para verificar a persistência.
        try (PessoaDAO dao = new PessoaDAO(nomeBanco)) {
            assertEquals(22, dao.buscarPorId(id).getIdade());
            assertTrue(dao.excluirPessoa(id));
            assertFalse(dao.excluirPessoa(id));
            assertNull(dao.buscarPorId(id));
        }
    }

    @Test
    void deveTratarIdsInexistentesEValidarRestricoesDoBanco() {
        try (PessoaDAO dao = new PessoaDAO(nomeBanco)) {
            assertNull(dao.buscarPorId(999999));
            assertFalse(dao.atualizarPessoa(999999, "X", 20, 1.7));
            assertFalse(dao.excluirPessoa(999999));
            assertThrows(IllegalStateException.class,
                    () -> dao.inserirPessoa(new Pessoa("Teste", -1, 1.75)));
            assertThrows(IllegalStateException.class,
                    () -> dao.inserirPessoa(new Pessoa("Teste", 21, 0)));
        }
    }
}
