# Tópicos de Big Data — Data Apps

Projeto didático complementar à apresentação **Data Apps para Big Data Analytics**.

## Objetivos

O material demonstra como transformar uma análise de dados em uma aplicação interativa sem misturar ingestão, regras analíticas e interface no mesmo arquivo.

O projeto cobre:

- Pandas;
- Plotly;
- Streamlit;
- Dash;
- organização em camadas;
- `st.cache_data`;
- `st.session_state`;
- `st.form`;
- navegação multipágina;
- validação de schema;
- testes com pytest;
- exemplo de camada curada com PySpark.

## Estrutura

```text
.
├── app.py
├── dash_app.py
├── spark_job.py
├── data/
│   └── supermarket_sales.csv
├── src/
│   ├── analytics.py
│   ├── charts.py
│   └── data.py
├── pages/
│   ├── overview.py
│   ├── explorer.py
│   └── about.py
├── examples/
├── tests/
├── .streamlit/
│   ├── config.toml
│   └── secrets.example.toml
└── requirements.txt
```

## 1. Ambiente virtual

### Windows

```bash
py -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## 2. Instalação

```bash
python -m pip install -r requirements.txt
```

## 3. Streamlit

```bash
python -m streamlit run app.py
```

## 4. Dash

```bash
python dash_app.py
```

## 5. Testes

```bash
python -m pytest -q
```

## 6. PySpark

O arquivo `spark_job.py` representa a etapa de processamento/curadoria em escala.

Ele **não** usa o CSV do exemplo Streamlit. O objetivo é mostrar o padrão:

```text
Data Lake
   ↓
Spark
   ↓
dados curados/agregados
   ↓
Data App
```

Para testar, instale PySpark e ajuste `input_path`/`output_path`.

## Boas práticas usadas

- funções pequenas;
- type hints;
- `Path`;
- validação de schema;
- `.loc[...]` + `.copy()` em filtros;
- transformação de datas explícita;
- cache para carregamento;
- estado apenas quando realmente necessário;
- secrets fora do código;
- analytics independentes da UI;
- testes das regras de dados;
- gráfico escolhido de acordo com a pergunta.

## Desafio para os alunos

Evolua o projeto com:

1. filtros adicionais;
2. um KPI novo;
3. uma visualização nova;
4. um teste automatizado novo;
5. uma análise de qualidade dos dados;
6. uma página adicional no Streamlit;
7. opcionalmente, uma fonte Parquet ou uma tabela curada pelo Spark.
