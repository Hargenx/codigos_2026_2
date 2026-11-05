package com.fintech.pagamento.model;

import java.time.LocalDateTime;
import java.util.Objects;

public class PagamentoPix extends Pagamento {
    private final String chavePix;
    private final String qrCode;

    public PagamentoPix(double valor, String chavePix, String qrCode) {
        super(valor);
        this.chavePix = Objects.requireNonNull(chavePix);
        this.qrCode = Objects.requireNonNull(qrCode);
    }

    public PagamentoPix(int id, String codigo, double valor, LocalDateTime data,
            String status, String chavePix, String qrCode) {
        super(id, codigo, valor, data, status);
        this.chavePix = Objects.requireNonNull(chavePix);
        this.qrCode = Objects.requireNonNull(qrCode);
    }

    public String getChavePix() {
        return chavePix;
    }

    public String getQrCode() {
        return qrCode;
    }

    @Override
    public double calcularTaxa() {
        return valor * 0.005;
    }

    @Override
    public String getTipo() {
        return "PIX";
    }
}
