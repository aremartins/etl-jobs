# Documentação de Erros e Soluções no Desenvolvimento do Projeto

## Índice
1. [Erro de Permissão no S3](#erro-de-permissão-no-s3)
2. [Problema com Encoding no CSV](#problema-com-encoding-no-csv)
3. [Correção de Path no Athena](#correção-de-path-no-athena)
4. [Coluna media sem valores no Glue Job](#coluna-media-sem-valores-no-glue-job)
5. [Problema com Encoding da Coluna Média](#problema-com-encoding-da-coluna-média)

## Erro de Permissão no S3

**Erro:** Access Denied ao tentar acessar objetos no S3.

**Causa:** As permissões do usuário ou role do IAM não estavam configuradas corretamente para permitir acesso ao bucket S3.

**Solução:** Verifique e ajuste as permissões da política IAM associada ao usuário ou role que está tentando acessar os dados no S3. A política correta deve incluir permissões para `s3:GetObject`, `s3:ListBucket`, `s3:PutObject`, e `s3:DeleteObject`.

**Exemplo de Política:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:DeleteObject",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:s3:::mybucket3s2",
        "arn:aws:s3:::mybucket3s2/*",
        "arn:aws:logs:*:*:*"
      ]
    }
  ]
}
```


## Problema com Encoding no CSV

**Erro:** A coluna média não era lida corretamente devido a caracteres especiais.

**Causa:** O encoding do arquivo CSV estava causando problemas na leitura de caracteres especiais.

**Solução:** Adicione a opção `.option("encoding", "UTF-8")` ao carregar o CSV no Spark.

**Código Ajustado:**
```python
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("encoding", "UTF-8") \
    .load("s3://mybucket3s2/dados/originais/dados_empresas.csv")
```

## Correção de Path no Athena

**Erro:** Path incorreto na definição da tabela no Athena.

**Causa:** Ao criar a tabela no Athena, foi especificado um path incorreto para o bucket S3.

**Solução:** Edite a tabela no Athena para apontar para o path correto no S3.

**Comando SQL Ajustado:**
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS customer_data.processed_data (
    empresa STRING,
    data TIMESTAMP,
    valor DOUBLE,
    cnpj STRING,
    ytd DOUBLE,
    media DOUBLE,
    data_int INT,
    valor_com_imposto DOUBLE
)
STORED AS PARQUET
LOCATION 's3://mybucket3s2/dados/processados/'
TBLPROPERTIES ("parquet.compression"="SNAPPY");
```

## Coluna media sem valores no Glue Job

**Erro:** A coluna media estava retornando valores nulos após o processamento.

**Causa:** A coluna no CSV estava com um nome diferente (média) que não correspondia ao nome utilizado no script do Glue Job.

**Solução:** Verifique e ajuste o nome da coluna no CSV e no script do Glue Job para garantir a correspondência.

**Código Ajustado:**
```python
df = df.withColumn("média", df["média"].cast("double"))
```

## Problema com Encoding da Coluna Média

**Erro:** A coluna Média estava com caracteres incorretos após o upload do CSV para o S3.

**Causa:** O arquivo CSV estava com problemas de encoding ao ser criado ou manipulado.

**Solução:** Verifique o encoding do arquivo CSV localmente antes de fazer o upload para o S3 e ajuste o encoding no script do Glue Job.

**Código Ajustado:**
```python
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("encoding", "UTF-8") \
    .load("s3://mybucket3s2/dados/originais/dados_empresas.csv")
