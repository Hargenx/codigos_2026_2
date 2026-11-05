package com.fintech.pagamento.model;

import java.time.LocalDateTime;
import java.util.Objects;
import java.util.UUID;

public abstract class Pagamento {
    protected int id;
    protected final String codigoTransacao;
    protected final double valor;
    protected final LocalDateTime dataHora;
    protected String status;

    protected Pagamento(double valor) {
        this(0, UUID.randomUUID().toString(), valor, LocalDateTime.now(), "PENDENTE");
    }

    protected Pagamento(int id, String codigoTransacao, double valor,
            LocalDateTime dataHora, String status) {
        if (!Double.isFinite(valor) || valor <= 0) {
            throw new IllegalArgumentException("Valor deve ser positivo e finito.");
        }
        this.id = id;
        this.codigoTransacao = Objects.requireNonNull(codigoTransacao);
        this.valor = valor;
        this.dataHora = Objects.requireNonNull(dataHora);
        this.status = Objects.requireNonNull(status);
    }

    public abstract double calcularTaxa();

    public abstract String getTipo();

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCodigoTransacao() {
        return codigoTransacao;
    }

    public double getValor() {
        return valor;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public String getStatus() {
        return status;
    }

    public double getValorLiquido() {
        return valor - calcularTaxa();
    }

    @Override
    public String toString() {
        return "%s{id=%d, codigo='%s', valor=%.2f, taxa=%.2f, liquido=%.2f, status='%s'}"
                .formatted(getTipo(), id, codigoTransacao, valor,
                        calcularTaxa(), getValorLiquido(), status);
    }
}
