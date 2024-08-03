# AWS Glue ETL Job

# Visão Geral
Este projeto envolve a criação de um job ETL (Extract, Transform, Load) utilizando AWS Glue para processar dados fictícios de empresas. Os dados são carregados de um arquivo CSV armazenado no S3, transformados e salvos de volta no S3 em formato Parquet.

# Estrutura do Projeto
```
etl-jobs/
├── scripts/
│ ├── processar_dados_empresas.py
│ └── explore_s3.py
└── data/
```
![imagem script na aws](https://github.com/aremartins/etl-jobs/blob/develop/imagens/bucket%20scripts%20dados%20empresas.jpg)<br><br>


# Descrição do Job

O job `processar_dados_empresas` executa as seguintes etapas:
 **Leitura dos Dados:** Carrega dados de um arquivo CSV armazenado no bucket S3 `mybucket3s2/dados/originais/dados_empresas.csv`.
 **Transformação dos Dados:**
   - Converte os tipos de dados das colunas.
   - Adiciona uma nova coluna com a data formatada como inteiro (`data_int`).
   - Adiciona uma nova coluna com o valor ajustado (`valor_com_imposto`).
 **Escrita dos Dados:** Salva os dados processados no bucket S3 `mybucket3s2/dados/processados/` em formato Parquet.<br><br>

# Passos para Executar o Job

## Criar o Job no AWS Glue

 Navegue até o console do AWS Glue e selecione "Jobs".
 Crie um novo job utilizando o script `processar_dados_empresas.py`.
 Configure o job para usar o IAM Role criado (`AWSGlueServiceRole`).
 
 ![glue job na aws](https://github.com/aremartins/etl-jobs/blob/develop/imagens/glue-job.jpg)<br><br>


 

## Executar o Job

1. Após a criação, execute o job diretamente pelo console do AWS Glue.
   
 ![execucao job na aws](https://github.com/aremartins/etl-jobs/blob/develop/imagens/job-success.jpg)<br><br>


 

## Verificar os Dados Processados

 Navegue até o bucket S3 `mybucket3s2/dados/processados/` para verificar os arquivos Parquet gerados.
 
 ![resultados athena](https://github.com/aremartins/etl-jobs/blob/develop/imagens/resultados%20athena%20s3.jpg)<br><br>


 

## Consultar os Dados com Athena

 No console do Athena, crie uma tabela externa apontando para os dados processados.
 Execute consultas SQL para verificar os dados processados.
```
SELECT * FROM customer_data.processed_data LIMIT 10;
```

![consulta athena na aws](https://github.com/aremartins/etl-jobs/blob/develop/imagens/consulta%20athena.jpg)<br>

---

![tabela criada athena](https://github.com/aremartins/etl-jobs/blob/develop/imagens/tabela%20criada%20results%20athena.jpg)<br><br>















## Atualizar o Glue Crawler
Para garantir que o catálogo do Glue esteja atualizado com os dados processados, rode o crawler configurado.

![crawlwer criado](https://github.com/aremartins/etl-jobs/blob/develop/imagens/crawler%20criado.jpg)

---

![crawler com sucesso](https://github.com/aremartins/etl-jobs/blob/develop/imagens/crawler%20com%20sucesso.jpg)<br><br>




## Catálogo do Glue

Verifique se o catálogo do Glue reflete as novas tabelas e dados.
![catálogo do Glue](https://github.com/aremartins/etl-jobs/blob/develop/imagens/tabela%20criada%20glue%20catalog.jpg)

---
Seguindo esses passos, você terá um pipeline completo de ETL utilizando AWS Glue, processando dados de um arquivo CSV, transformando-os e armazenando-os em formato Parquet no S3, além de consultá-los utilizando AWS Athena.
