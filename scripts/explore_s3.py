import boto3;
import pandas as pd;

session = boto3.Session()

s3 = session.client('s3')

buckets = [
    'my-company-data-athena-results',
    'my-company-data-raw-customers',
    'my-company-data-raw-logs',
    'my-company-data-raw-transactions',
    'mybucket3s2'
]

for bucket in buckets:
    print(f'Conteúdo do bucket: {bucket}')
    response = s3.list_objects_v2(Bucket=bucket)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else: 
        print("O bucket está vazio.")
    print("\n")


bucket_name = 'mybucket3s2'

response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(obj['Key'])

object_key = 'dados/originais/dados_empresas.csv'

s3.download_file(bucket_name, object_key, 'dados_empresas.csv')

data = pd.read_csv('dados_empresas.csv')
print(data.head())
