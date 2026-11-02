# RAD em Python — Aula 10 (novembro de 2026)

Projeto didático da disciplina **Desenvolvimento Rápido de Aplicações em Python**, para graduação em Sistemas de Informação, Ciência da Computação e Análise e Desenvolvimento de Sistemas.

## O que aprenderemos

- Criar uma interface gráfica com `tkinter` e `ttk`.
- Exibir registros em uma tabela com `ttk.Treeview`.
- Persistir dados localmente usando `sqlite3`.
- Implementar as quatro operações CRUD: **Create, Read, Update, Delete**.
- Separar interface (`main.py`) de persistência (`database.py`) com classes simples.
- Aplicar instruções SQL parametrizadas e tratar e-mail duplicado.

## Requisitos

- Python **3.11 ou superior** com suporte a Tkinter. Não requer pacotes do `pip`.
- Windows, macOS ou Linux com ambiente gráfico. Em algumas distribuições Linux, Tkinter precisa ser instalado pelo gerenciador de pacotes.

Para conferir se Tkinter está disponível:

```bash
python -m tkinter
```

## Como executar

Entre nesta pasta e rode:

```bash
python exemplo_treeview.py
python main.py
```

No Windows, se `python` não funcionar, tente `py`.

O arquivo `usuarios.db` será criado automaticamente **na mesma pasta de `main.py`** quando a aplicação principal iniciar. Os dados persistem depois de fechar a janela.

## Estrutura

```text
RAD_2026_10_codigo/
├── database.py            # SQLite: criação da tabela e operações CRUD
├── main.py                # Tela principal e formulário de cadastro
├── exemplo_treeview.py    # Primeiro Treeview sem banco de dados
├── tests/
│   └── test_database.py   # Testes do banco, sem abrir janelas
└── README.md
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Roteiro sugerido

1. Execute `exemplo_treeview.py` e identifique cabeçalhos, colunas e registros.
2. Execute `main.py`; cadastre dois usuários com e-mails diferentes.
3. Feche e reabra o programa. Os registros devem continuar no banco.
4. Edite o nome de um usuário, depois exclua outro.
5. Cadastre um e-mail duplicado e observe `sqlite3.IntegrityError` sendo tratado.
6. Altere o código para adicionar **pesquisa por nome** usando `LIKE ?` e o botão "Buscar" (exercício proposto nos slides).

## Pontos de atenção

- `with self.conn:` controla a confirmação (commit) ou desfazimento (rollback) da transação, **mas não fecha a conexão**. Por isso, `banco.fechar()` é chamado ao final do programa.
- Os marcadores `?` protegem os valores de consultas parametrizadas; evite montar SQL concatenando valores digitados pelo usuário.
- Este é um exemplo local e didático. O formulário só exige valores não vazios: **não valida se o e-mail existe de verdade**.
- Não altere o arquivo SQLite manualmente enquanto o programa estiver aberto.

## Referências

- Documentação oficial do `tkinter.ttk`: <https://docs.python.org/3.14/library/tkinter.ttk.html>
- Documentação oficial do `sqlite3`: <https://docs.python.org/3.14/library/sqlite3.html>
- Repositório de exemplos complementares do professor: <https://github.com/professorRaphael/Exemplos_para_o_trabalho_RAD>

O repositório acima é material **complementar** e não é necessário para executar este projeto.
