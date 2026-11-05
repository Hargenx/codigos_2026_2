package com.fintech.pagamento.model;

import java.time.LocalDateTime;
import java.util.Objects;

public class PagamentoCartao extends Pagamento {
    private final String numeroCartaoMascarado;
    private final String bandeira;
    private final int parcelas;

    public PagamentoCartao(double valor, String numeroCartaoMascarado,
            String bandeira, int parcelas) {
        super(valor);
        this.numeroCartaoMascarado = Objects.requireNonNull(numeroCartaoMascarado);
        this.bandeira = Objects.requireNonNull(bandeira);
        this.parcelas = validarParcelas(parcelas);
    }

    public PagamentoCartao(int id, String codigo, double valor, LocalDateTime data,
            String status, String numeroCartaoMascarado,
            String bandeira, int parcelas) {
        super(id, codigo, valor, data, status);
        this.numeroCartaoMascarado = Objects.requireNonNull(numeroCartaoMascarado);
        this.bandeira = Objects.requireNonNull(bandeira);
        this.parcelas = validarParcelas(parcelas);
    }

    private static int validarParcelas(int parcelas) {
        if (parcelas < 1)
            throw new IllegalArgumentException("Parcelas >= 1.");
        return parcelas;
    }

    public String getNumeroCartaoMascarado() {
        return numeroCartaoMascarado;
    }

    public String getBandeira() {
        return bandeira;
    }

    public int getParcelas() {
        return parcelas;
    }

    @Override
    public double calcularTaxa() {
        return valor * (0.025 + 0.01 * parcelas);
    }

    @Override
    public String getTipo() {
        return "CARTAO";
    }
}
