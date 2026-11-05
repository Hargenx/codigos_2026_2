# Gabarito 1 — Gateway de Pagamentos

**Java 17 (LTS), Maven, JDBC/SQLite.** Projeto independente referente ao Exercício 1 do HTML.

## Executar

Use um JDK 47 ativo (`JAVA_HOME` apontando para o JDK 17).

```bash
mvn clean compile exec:java
```

Na pasta do projeto, o SQLite criará `db/financeiro.db` (dados persistem entre execuções).

## Conceitos

- Classe abstrata `Pagamento` e subclasses PIX, cartão e boleto.
- Polimorfismo em `calcularTaxa()`, `getTipo()` e `getValorLiquido()`.
- DAO com tabela única e coluna discriminadora `tipo_pagamento`.
- `salvar`, `listarTodos` e `buscarPorCodigo` reconstituem os tipos concretos.
- `PreparedStatement` e fechamento seguro com `try-with-resources`.

## Premissas do gabarito

- Taxa do cartão: **2,5% + 1 ponto percentual por parcela** (3 parcelas = 5,5%).
- Como o enunciado exige `double`, ele foi mantido. Em pagamentos de produção, prefira `BigDecimal` ou valores inteiros em centavos para evitar problemas de arredondamento.
- Os valores e identificadores apresentados na `Main` são demonstrativos. Cada execução cria novos pagamentos, com UUIDs diferentes.
