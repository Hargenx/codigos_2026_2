package com.fintech.pagamento.model;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Objects;

public class PagamentoBoleto extends Pagamento {
    private final String codigoBarras;
    private final LocalDate dataVencimento;

    public PagamentoBoleto(double valor, String codigoBarras, LocalDate dataVencimento) {
        super(valor);
        this.codigoBarras = Objects.requireNonNull(codigoBarras);
        this.dataVencimento = Objects.requireNonNull(dataVencimento);
    }

    public PagamentoBoleto(int id, String codigo, double valor, LocalDateTime data,
            String status, String codigoBarras, LocalDate vencimento) {
        super(id, codigo, valor, data, status);
        this.codigoBarras = Objects.requireNonNull(codigoBarras);
        this.dataVencimento = Objects.requireNonNull(vencimento);
    }

    public String getCodigoBarras() {
        return codigoBarras;
    }

    public LocalDate getDataVencimento() {
        return dataVencimento;
    }

    @Override
    public double calcularTaxa() {
        return 2.50;
    }

    @Override
    public String getTipo() {
        return "BOLETO";
    }
}
