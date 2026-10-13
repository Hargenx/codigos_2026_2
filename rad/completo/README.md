# Python + SQLite — CRUD com Persistência de Dados

Projeto desenvolvido para fins didáticos na disciplina de **Desenvolvimento Rápido de Aplicações em Python**, em turma de **Graduação**.

O objetivo deste projeto é demonstrar, de forma prática, como uma aplicação Python pode trabalhar com persistência de dados utilizando **SQLite**, aplicando conceitos como:

- orientação a objetos;
- `dataclasses`;
- conexão com banco de dados;
- criação de tabelas;
- relacionamentos;
- chaves primárias e estrangeiras;
- operações CRUD;
- consultas SQL;
- `JOIN`;
- tratamento de exceções;
- logging;
- parametrização de queries;
- organização inicial de um projeto Python.

> Este projeto foi desenvolvido como material de apoio para aula e **não representa uma aplicação finalizada**. A intenção é justamente que ele possa ser analisado, modificado, refatorado e evoluído pelos alunos ao longo da disciplina.

---

## Objetivo do projeto

A aplicação representa um pequeno sistema de cadastro envolvendo três entidades:

- **Pessoa**
- **Marca**
- **Veículo**

Uma pessoa pode ser proprietária de veículos, enquanto cada veículo possui uma marca associada.

O projeto utiliza classes Python para representar essas entidades e o SQLite para armazenar os dados de forma persistente.

Exemplo simplificado do relacionamento:

```text
Pessoa
  |
  | possui
  |
  v
Veículo ------> Marca
```

---

## Estrutura do projeto

Uma possível organização dos arquivos é:

```text
projeto/
│
├── banco.py
├── logger_config.py
├── main.py
├── marca.py
├── pessoa.py
├── veiculo.py
│
├── logs/
│   └── app.log
│
└── banco.sqlite
```

### `pessoa.py`

Define a classe `Pessoa`.

```python
@dataclass(slots=True)
class Pessoa:
    cpf: str
    nome: str
    nascimento: date
    oculos: bool
    multas: list[str] = field(default_factory=list)
```

---

### `marca.py`

Define a classe `Marca`.

```python
@dataclass(slots=True, frozen=True)
class Marca:
    id: int
    nome: str
    sigla: str
```

Nesse exemplo, a classe foi definida como `frozen=True`, tornando suas instâncias imutáveis após a criação.

---

### `veiculo.py`

Representa um veículo e mantém referências para seu proprietário e sua marca.

```python
@dataclass(slots=True)
class Veiculo:
    placa: str
    cor: str
    proprietario: Pessoa
    marca: Marca
```

---

### `banco.py`

Responsável pelo acesso ao banco de dados.

A classe `BancoDeDados` concentra operações como:

```text
conectar()
criar_tabelas()

inserir_pessoa()
inserir_marca()
inserir_veiculo()

atualizar_pessoa()
atualizar_veiculo()

apagar_pessoa()
apagar_veiculo()

buscar_pessoa_por_cpf()
buscar_marca_por_id()
buscar_veiculo_por_placa()

buscar_todas_pessoas()
buscar_todas_marcas()
buscar_todos_veiculos()

buscar_veiculos_da_pessoa()
```

Também são tratados erros relacionados ao SQLite e realizados registros utilizando `logging`.

---

### `logger_config.py`

Centraliza a configuração do sistema de logs.

Os registros são enviados para:

```text
logs/app.log
```

e também podem ser exibidos no terminal.

Exemplo:

```text
2026-10-12 20:30:15 | INFO | rad_python | Conexão com o banco realizada com sucesso.
```

O uso de logging permite registrar informações importantes da aplicação sem depender apenas de `print()`.

---

### `main.py`

É o ponto inicial da aplicação.

Nele são demonstradas operações como:

- criação dos objetos;
- conexão com o banco;
- criação das tabelas;
- inserção de registros;
- consultas;
- atualizações;
- relacionamentos;
- consultas utilizando `JOIN`.

---

## Banco de dados

O projeto utiliza o módulo:

```python
sqlite3
```

que já faz parte da biblioteca padrão do Python.

Portanto, não é necessário instalar um servidor de banco de dados separado.

O banco é armazenado em um arquivo local:

```text
banco.sqlite
```

---

## Relacionamentos

A tabela `Veiculo` possui referências para `Pessoa` e `Marca`.

```sql
FOREIGN KEY (cpf_proprietario)
    REFERENCES Pessoa(cpf)

FOREIGN KEY (id_marca)
    REFERENCES Marca(id)
```

A aplicação também habilita explicitamente a verificação de chaves estrangeiras do SQLite:

```python
conn.execute("PRAGMA foreign_keys = ON")
```

---

## Operações CRUD

Durante as aulas são exploradas as quatro operações fundamentais utilizadas em aplicações que trabalham com persistência de dados.

## CREATE

Inserção de registros.

```sql
INSERT INTO Pessoa (
    cpf,
    nome,
    nascimento,
    oculos
)
VALUES (?, ?, ?, ?)
```

---

## READ

Consulta de registros.

```sql
SELECT
    cpf,
    nome,
    nascimento,
    oculos
FROM Pessoa
```

---

## UPDATE

Atualização de registros.

```sql
UPDATE Pessoa
SET
    nome = ?,
    nascimento = ?,
    oculos = ?
WHERE cpf = ?
```

---

## DELETE

Remoção de registros.

```sql
DELETE FROM Pessoa
WHERE cpf = ?
```

---

## Queries parametrizadas

As consultas do projeto utilizam parâmetros:

```python
cursor.execute(
    "SELECT * FROM Pessoa WHERE cpf = ?",
    (cpf,),
)
```

Evite construir comandos SQL concatenando diretamente valores fornecidos pelo usuário.

Por exemplo:

```python
# EVITE
sql = f"SELECT * FROM Pessoa WHERE cpf = '{cpf}'"
```

Prefira sempre que possível:

```python
sql = "SELECT * FROM Pessoa WHERE cpf = ?"
cursor.execute(sql, (cpf,))
```

Além de deixar o código mais organizado, isso reduz problemas relacionados a **SQL Injection**.

---

## Consultas com JOIN

O projeto também demonstra como recuperar informações relacionadas utilizando `JOIN`.

Exemplo:

```sql
SELECT
    v.placa,
    v.cor,

    p.cpf,
    p.nome,

    m.id,
    m.nome

FROM Veiculo AS v

INNER JOIN Pessoa AS p
    ON p.cpf = v.cpf_proprietario

INNER JOIN Marca AS m
    ON m.id = v.id_marca
```

Esse tipo de consulta permite recuperar, em uma única operação, informações de várias tabelas relacionadas.

---

## Executando o projeto

É recomendado utilizar uma versão recente do Python.

Verifique a instalação:

```bash
python --version
```

ou:

```bash
py --version
```

Clone ou baixe o projeto e acesse sua pasta:

```bash
cd nome-do-projeto
```

Execute:

```bash
python main.py
```

No Windows também pode ser utilizado:

```bash
py main.py
```

Na primeira execução, o arquivo:

```text
banco.sqlite
```

será criado automaticamente caso ainda não exista.

---

## Ambiente virtual

Embora este projeto utilize inicialmente apenas recursos da biblioteca padrão do Python, é uma boa prática trabalhar com ambientes virtuais.

Criando o ambiente:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

---

## Importante: este projeto não termina aqui

A versão apresentada em aula foi mantida propositalmente simples para facilitar a visualização dos conceitos estudados.

Entretanto, conforme uma aplicação cresce, concentrar muitas responsabilidades em poucas classes deixa de ser uma solução adequada.

Por isso, um dos objetivos da disciplina é que os alunos **continuem evoluindo o projeto**.

Algumas melhorias possíveis são:

- aumentar a modularização;
- separar responsabilidades;
- criar camadas específicas para acesso a dados;
- utilizar Repository;
- criar uma camada de serviços;
- implementar regras de negócio;
- aplicar uma arquitetura de software;
- melhorar validações;
- criar exceções próprias;
- adicionar testes automatizados;
- utilizar arquivos de configuração;
- implementar migrations;
- utilizar um ORM;
- criar uma API;
- desenvolver uma interface gráfica ou aplicação web.

---

## Um possível próximo passo

Atualmente temos algo próximo de:

```text
main.py
   |
   v
BancoDeDados
   |
   v
SQLite
```

Uma evolução possível seria:

```text
Interface
    |
    v
Services
    |
    v
Repositories
    |
    v
SQLite
```

Com os modelos separados:

```text
models/
├── pessoa.py
├── marca.py
└── veiculo.py
```

E uma estrutura semelhante a:

```text
projeto/
│
├── app/
│   │
│   ├── models/
│   │   ├── pessoa.py
│   │   ├── marca.py
│   │   └── veiculo.py
│   │
│   ├── repositories/
│   │   ├── pessoa_repository.py
│   │   ├── marca_repository.py
│   │   └── veiculo_repository.py
│   │
│   ├── services/
│   │   └── ...
│   │
│   ├── database/
│   │   └── database.py
│   │
│   └── ...
│
├── tests/
│
├── main.py
└── README.md
```

Essa é apenas uma possibilidade.

Parte do exercício é justamente discutir **quando e por que uma aplicação precisa ser reorganizada**.

---

## Próxima aula: Front-end

Na próxima etapa da disciplina, este projeto será utilizado como base para adicionar uma **interface para o usuário**.

Até este momento, a interação acontece principalmente através do terminal:

```text
Usuário
   |
   v
Terminal
   |
   v
Python
   |
   v
SQLite
```

A próxima evolução será algo semelhante a:

```text
Usuário
   |
   v
Front-end
   |
   v
Aplicação Python
   |
   v
Banco de Dados
```

A ideia não é abandonar o código desenvolvido até aqui.

Pelo contrário: o desafio será **adaptar e organizar o projeto para que a interface utilize as funcionalidades que já foram implementadas**.

Isso naturalmente levantará novas questões:

- O front-end deve acessar o banco diretamente?
- Onde devem ficar as regras de negócio?
- A classe `BancoDeDados` está fazendo coisas demais?
- Devemos separar cada entidade em um repositório?
- Como evitar duplicação?
- Como tratar erros que precisam ser apresentados ao usuário?
- Como organizar o projeto para que ele possa crescer?

Essas perguntas fazem parte da evolução natural de um projeto de software.

---

## Desafio

Antes da próxima aula, analise o projeto e pense:

> **Se esse sistema precisasse crescer e receber dezenas de novas funcionalidades, você manteria a estrutura atual?**

Escolha pelo menos uma melhoria que você faria no projeto.

Algumas possibilidades:

```text
[ ] Modularizar melhor o código
[ ] Separar acesso ao banco de dados
[ ] Criar repositories
[ ] Criar services
[ ] Melhorar o tratamento de erros
[ ] Criar testes
[ ] Melhorar validações
[ ] Adicionar novas entidades
[ ] Criar uma arquitetura para a aplicação
[ ] Pensar em como conectar um front-end
```

Não existe uma única resposta correta.

O importante é conseguir **justificar tecnicamente as decisões tomadas**.

---

## Aviso acadêmico

Este projeto foi desenvolvido como material de apoio para a disciplina de:

- **Desenvolvimento Rápido de Aplicações em Python**

em cursos de **Graduação**.

O código possui finalidade educacional e foi estruturado para permitir que conceitos sejam apresentados progressivamente em sala de aula.

Ele não deve ser tratado como uma arquitetura definitiva ou como um modelo pronto para utilização em produção.

A proposta é exatamente o contrário:

> **entender o código atual, identificar suas limitações e evoluí-lo conforme novos conceitos forem apresentados.**

---

## Professor

- **Prof. Raphael M. S. de Jesus**

Disciplina: **Desenvolvimento Rápido de Aplicações em Python**
