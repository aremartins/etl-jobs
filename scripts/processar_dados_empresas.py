import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, date_format, lit

# Captura os argumentos do job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Inicializa o contexto Spark e Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Carrega os dados do S3
df = spark.read.format("csv") \
    .option("header", "true") \
    .load("s3://mybucket3s2/dados/originais/dados_empresas.csv")

# Converte os tipos de dados das colunas
df = df.withColumn("data", df["data"].cast("timestamp")) \
       .withColumn("valor", df["valor"].cast("double")) \
       .withColumn("cnpj", df["cnpj"].cast("string")) \
       .withColumn("ytd", df["ytd"].cast("double")) \
       .withColumn("média", df["média"].cast("double"))

# Adiciona nova coluna com a data formatada como inteiro
df_transformed = df.withColumn("data_int", date_format(col("data"), "yyyyMMdd").cast("int"))

# Adiciona nova coluna com valor ajustado
df_transformed = df_transformed.withColumn("valor_com_imposto", col("valor") * lit(1.10))

# Escreve os dados processados de volta no S3 em formato Parquet
df_transformed.write.mode("overwrite").parquet("s3://mybucket3s2/dados/processados/")

# Finaliza o job
job.commit()
