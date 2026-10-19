package com.aula_poo;

public class Pessoa {
    private int id;
    private String nome;
    private int idade;
    private double altura;

    public Pessoa(String nome, int idade, double altura) {
        this(0, nome, idade, altura);
    }

    public Pessoa(int id, String nome, int idade, double altura) {
        this.id = id;
        this.nome = nome;
        this.idade = idade;
        this.altura = altura;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public int getIdade() { return idade; }
    public void setIdade(int idade) { this.idade = idade; }
    public double getAltura() { return altura; }
    public void setAltura(double altura) { this.altura = altura; }

    @Override
    public String toString() {
        return "Pessoa{id=" + id + ", nome='" + nome + "', idade=" + idade
                + ", altura=" + altura + "}";
    }
}
