from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main() -> None:
    spark = (
        SparkSession.builder
        .appName(
            "BigDataAnalyticsCurated"
        )
        .getOrCreate()
    )

    # Em produção, substitua pelos caminhos reais do Data Lake.
    input_path = "data_lake/vendas/"
    output_path = "curated/vendas_mes_regiao/"

    df = spark.read.parquet(
        input_path
    )

    resumo = (
        df
        .filter(
            F.col("valor") > 0
        )
        .withColumn(
            "mes",
            F.date_trunc(
                "month",
                F.col("data")
            )
        )
        .groupBy(
            "mes",
            "regiao"
        )
        .agg(
            F.sum(
                "valor"
            ).alias(
                "faturamento"
            ),
            F.countDistinct(
                "pedido_id"
            ).alias(
                "pedidos"
            ),
        )
    )

    (
        resumo
        .write
        .mode("overwrite")
        .partitionBy("mes")
        .parquet(
            output_path
        )
    )

    spark.stop()


if __name__ == "__main__":
    main()
