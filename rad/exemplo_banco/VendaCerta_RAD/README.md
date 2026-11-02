# VendaCerta — PDV didático de uma pequena loja de informática

**Disciplina:** Desenvolvimento Rápido de Aplicações em Python (RAD)  
**Público:** cursos de graduação em Computação, Sistemas de Informação e Análise e Desenvolvimento de Sistemas.  
**Professor:** Raphael Mauricio Sanches de Jesus.  
**Projeto:** exemplo novo para complementar o repositório `professorRaphael/Exemplos_RAD`.

> **Escopo:** protótipo educacional **offline** para operação em um único computador. Não é um sistema fiscal, ERP, gateway de pagamento ou solução pronta para produção. Não emite NFC-e/NF-e, não processa pagamentos, não mantém trilha formal de auditoria de estoque e não foi feito para vários caixas simultâneos.

## 1. Situação-problema

Uma pequena loja de informática realiza vendas no balcão. O dono tem dificuldade para saber o que ainda existe no estoque, conferir os preços praticados e consultar vendas anteriores. Uma planilha é possível, mas uma venda com vários produtos exige atualizar diferentes registros **como uma única operação**.

Neste exemplo, a turma implementa o processo operacional de uma loja: **produto → entrada em estoque → carrinho → venda → baixa de estoque → histórico → possível cancelamento**.

O foco não é somente CRUD de pessoas ou livros: cada ação tem consequências em outras tabelas.

## 2. Funcionalidades

- Cadastrar e editar SKU, nome, preço de venda e estoque mínimo.
- Informar estoque inicial no cadastro e registrar recebimento de mercadorias (a edição de dados não altera o saldo).
- Destacar produtos com saldo menor ou igual ao mínimo definido.
- Adicionar **vários produtos à mesma venda**, com quantidades e total calculado.
- Persistir venda e itens no banco; baixar estoque apenas se houver saldo para **todos** os itens.
- Impedir estoque negativo. Se uma linha falhar, a venda inteira é desfeita (transação SQLite).
- Consultar histórico e itens de cada venda.
- Cancelar a venda **uma única vez**, devolvendo as quantidades ao estoque; o registro permanece como `CANCELADA`.
- Preservar descrição e preço da época da venda nos itens históricos (preço *snapshot*).
- Exibir faturamento registrado (soma das vendas concluídas), número de vendas e alertas de reposição.
- Exportar o histórico de vendas em CSV com separador `;`, legível no Excel.
- Carregar um catálogo **fictício** de cinco produtos para demonstração, apenas em banco vazio.

## Capturas da interface

As capturas demonstram a interface em operação, com dados fictícios:

- [Cadastro e estoque](capturas/preview_produtos.png)
- [Venda com carrinho](capturas/preview_venda.png)
- [Histórico de vendas](capturas/preview_historico.png)

## 3. Tecnologias e arquitetura

Python **3.10+** e exclusivamente biblioteca padrão:

- `tkinter` / `ttk`: janelas, abas, campos e tabelas `Treeview`;
- `sqlite3`: persistência e transações;
- `decimal` + valores inteiros em centavos: dinheiro sem uso de `float` nos cálculos;
- `unittest`: testes automatizados;
- `csv`: exportação de dados.

Divisão simples de responsabilidades, sem frameworks ou arquitetura desnecessária:

```text
VendaCerta_RAD/
├── main.py                # Abre a aplicação
├── banco.py               # Conexão SQLite e criação das tabelas
├── negocio.py             # Regras, validações e operações de venda
├── interface.py           # Interface Tkinter/ttk
├── tests/
│   └── test_negocio.py   # Testes automatizados sem interface
├── ENUNCIADO.md           # Exercício sugerido para a turma
├── capturas/              # Telas com dados fictícios
├── .gitignore
└── README.md
```

A pasta `dados/` com o arquivo `vendacerta.sqlite3` é criada na **primeira execução**; não é incluída no projeto distribuído.

## 4. Como executar

1. Instale o Python 3.10 ou superior. No Windows, utilize o instalador oficial com Tkinter habilitado.
2. Extraia o ZIP e abra um terminal **dentro da pasta `VendaCerta_RAD`**.
3. Execute:

```bash
python main.py
```

No Windows, também é possível usar `py main.py` (se o Python Launcher estiver instalado). No Linux, utilize `python3 main.py` e instale o pacote de sistema `python3-tk` se o módulo Tkinter não estiver disponível.

**Nenhum `pip install` é necessário.**

### Primeiro teste na interface

1. Acesse **Produtos e estoque** e clique em **Carregar catálogo demonstrativo** (opcional).
2. Em **Nova venda**, selecione `Mouse USB`, informe quantidade `2` e clique em **Adicionar**.
3. Adicione também `Cabo HDMI 2 m`, quantidade `1`.
4. Clique em **Finalizar venda**. Confira o total e a redução de estoque.
5. Em **Histórico**, selecione a venda e veja suas linhas.
6. Clique em **Cancelar venda selecionada**. O status muda e o estoque é devolvido.

**Atenção:** produtos e vendas fictícios persistem no SQLite. Para reiniciar a demonstração, feche a aplicação e apague somente o arquivo `dados/vendacerta.sqlite3`. Isso descarta todos os dados armazenados nele.

## 5. Regras de negócio importantes

| Código | Regra | Por quê? |
| --- | --- | --- |
| RN01 | SKU de produto é único | Evita cadastro duplicado de mercadoria |
| RN02 | Preço deve ser positivo; saldo e mínimo não negativos | Evita dados incoerentes |
| RN03 | Quantidades vendidas são inteiras e positivas | Cada item representa unidades físicas |
| RN04 | Venda só acontece com saldo para **todos os itens** | Não pode gerar meia venda por erro de estoque |
| RN05 | Venda concluída reduz estoque na mesma transação | Protege a consistência |
| RN06 | Cancelamento é único e repõe estoque | Evita reposição duplicada |
| RN07 | Item vendido guarda preço e nome históricos | Mudanças no catálogo não alteram a venda antiga |
| RN08 | Faturamento ignora vendas canceladas | Evita inflar a soma de vendas válidas |

**Exemplo:** uma venda contém dois mouses e três teclados, mas só há um teclado disponível. O sistema não grava venda, não reduz os dois mouses e mostra o erro de saldo.

### Dinheiro no banco

Um item de **R$ 89,90** é armazenado como **8.990 centavos**. O total de duas unidades é `2 × 8990 = 17980` centavos. `float` não participa dos cálculos de venda. As entradas aceitam `89,90` ou `89.90` e não aceitam separador de milhar.

### Tabelas

- `produtos`: catálogo e saldo atual;
- `vendas`: cliente, data/hora, status e total;
- `itens_venda`: ligação entre venda e produtos, quantidades e preços congelados.

## 6. Executar testes

Na pasta do projeto:

```bash
python -m unittest discover -s tests -v
```

São **14 testes** de validação, estoque, vendas, reversão, consistência e histórico. Os testes usam arquivos SQLite temporários e **não modificam** o banco usado pela interface.

## 7. Plano de aula sugerido (aprox. 2h50)

| Etapa | Tempo | Atividade |
| --- | ---: | --- |
| Contextualização | 20 min | Por que um pedido precisa de várias tabelas? |
| Banco de dados | 35 min | Interpretar as três tabelas e as chaves estrangeiras |
| Regras de negócio | 45 min | Ler `vender()`, discutir transações e saldo |
| Interface | 35 min | Acompanhar `ttk.Notebook` e `ttk.Treeview` |
| Experimentação | 25 min | Fazer venda, testar falta de estoque, cancelar |
| Desafio e fechamento | 10 min | Propor melhoria de filtro do histórico |

## 8. Limitações propositais e evolução

Para permanecer simples e demonstrável em sala:

- Não há registro contábil de pagamento ou conciliação bancária; o termo **faturamento** refere-se apenas à soma das vendas concluídas no protótipo.
- O cancelamento representa uma reversão operacional da venda, **não** estorno de cartão, devolução fiscal ou geração de documentos oficiais.
- Recebimentos de estoque são somados ao saldo, mas ainda **não** há uma tabela de movimentos com operador, motivo e data (sugestão de trabalho).
- Não há autenticação, permissões, impostos, descontos, fornecedores, custos ou multiusuário.
- O banco local não usa criptografia nem oferece sincronização em nuvem. Não utilize dados pessoais reais para exercícios.

Como evolução de aula, adicione filtro de histórico por cliente e data, relatório de produtos em reposição e movimentações de estoque com rastreabilidade. O arquivo `ENUNCIADO.md` contém uma proposta objetiva.

## 9. Referências técnicas

- [Python — Tkinter/ttk](https://docs.python.org/3/library/tkinter.ttk.html)
- [Python — sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Python — unittest](https://docs.python.org/3/library/unittest.html)
- [Repositório de exemplos RAD](https://github.com/professorRaphael/Exemplos_RAD)

---

**Material didático.** O projeto é original para este exercício e foi concebido para estudo e adaptação por alunos de graduação.
