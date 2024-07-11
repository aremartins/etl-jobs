import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, date_format, lit

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_options(
    "s3",
    {"paths": ["s3://mybucket3s2/dados/originais/dados_empresas.csv"]},
    format="csv",
    format_options={"withHeader": True}
)

applymapping1 = ApplyMapping.apply(
    frame=datasource0, 
    mappings=[
        ("empresa", "string", "empresa", "string"),
        ("data", "string", "data", "timestamp"),
        ("valor", "bigint", "valor", "double"),
        ("cnpj", "bigint", "cnpj", "string"),
        ("ytd", "bigint", "ytd", "double"),
        ("média", "bigint", "media", "double")
    ]
)

df = applymapping1.toDF()

df_transformed = df.withColumn("data_int", date_format(col("data"), "yyyyMMdd").cast("int"))

df_transformed = df_transformed.withColumn("valor_com_imposto", col("valor") * lit(1.10))

dynamic_frame_transformed = DynamicFrame.fromDF(df_transformed, glueContext, "dynamic_frame_transformed")

datasink2 = glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_transformed,
    connection_type="s3",
    connection_options={"path": "s3://mybucket3s2/dados/processados/"},
    format="parquet"
)

job.commit()
