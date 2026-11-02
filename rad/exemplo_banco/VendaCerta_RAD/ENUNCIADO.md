# Desafio RAD — VendaCerta: uma loja que não pode vender estoque negativo

## Situação realista

Uma loja de informática comercializa acessórios no balcão. Um único atendimento pode incluir três cabos HDMI, um SSD e dois teclados. O estoque precisa ser atualizado na confirmação; a gerência consulta o histórico e, quando necessário, cancela uma venda.

Você recebeu um sistema desktop simples e funcional, feito com Python, Tkinter e SQLite. Seu trabalho é **entender as regras existentes e desenvolver uma melhoria pequena e verificável**, não reescrever a aplicação inteira.

## Etapa 1 — Estudo e exploração

1. Abra `main.py`, `banco.py`, `negocio.py` e `interface.py`. Identifique a função de cada arquivo.
2. Cadastre um produto, altere seu preço e registre cinco unidades de entrada.
3. Venda duas unidades. Confira o saldo antes e depois.
4. Tente vender mais unidades do que existem. Qual dado mudou no banco?
5. Cancele a venda. Por que o sistema não permite cancelá-la novamente?
6. Altere o preço de um produto já vendido. O preço da venda antiga mudou? Explique.

## Etapa 2 — Desafio principal: filtro de vendas

**Implemente uma pesquisa por nome do cliente na aba Histórico**.

### Requisitos

- R01: Campo de pesquisa aceita parte do nome, sem diferenciar maiúsculas/minúsculas.
- R02: A tabela lista somente vendas que correspondem ao texto informado.
- R03: Botão **Limpar pesquisa** restaura todas as vendas.
- R04: Ao filtrar, as tabelas de itens não devem mostrar registros de outra venda.
- R05: A consulta SQL deve utilizar parâmetros `?`, sem concatenar texto do usuário diretamente à instrução SQL.

### Dicas (sem gabarito completo)

- Crie um método `pesquisar_vendas(texto)` na classe `Loja`.
- Utilize `WHERE cliente LIKE ?` com o padrão `%texto%` passado como parâmetro.
- Integre uma entrada de texto e um botão à interface de Histórico.
- Crie dois testes: pesquisa com correspondência e sem correspondência.

## Etapa 3 — Extensões opcionais

- **Básica:** ordenar catálogo por menor estoque e contar produtos para reposição.
- **Intermediária:** exportar relatório CSV de itens vendidos com quantidade e valor.
- **Avançada:** criar tabela `movimentos_estoque` com produto, tipo, quantidade, data/hora e motivo. Registrar recebimentos, vendas e cancelamentos na **mesma transação** que altera o saldo.

## Critérios de avaliação sugeridos (10 pontos)

| Critério | Peso |
| --- | ---: |
| Funcionalidade: busca e limpeza corretas | 3,0 |
| Uso seguro de SQL parametrizado | 2,0 |
| Clareza e simplicidade do código | 2,0 |
| Dois testes automatizados novos | 2,0 |
| README atualizado com instruções | 1,0 |

**Entrega:** pasta do projeto ou link do repositório do aluno, comandos de execução e breve demonstração em vídeo ou sala. Não inclua banco com dados pessoais reais.
