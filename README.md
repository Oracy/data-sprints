# Data Sprints

## Estrutura usada para o projeto

- A estrutura utilizada foi a stack da AWS.
- Para armazenamento dos dados usei S3.
- Para subir o airflow usei terraform.
- A maquina foi uma ec2 t3a.xlarge
- Para visualização dos dados usei QuickSight, nao consigo disponibilizar para publico o dashboard, mas esta pronto na minha conta, e consigo dar permissão para usuarios.

## Terraform

Repositório [terraform](./airflow_aws).
Para iniciar o projeto terraform, é necessario ter os acessos a AWS com `aws_key_id` e `aws_secret_access_key`.
Rodar os comandos `terraform init && terraform plan && terraform apply`.
`terraform plan` nao é um comando essencial, apenas para ver quais alteracoes irao ocorrer.

## Fluxo Airflow

[Fluxo_Airflow](data_sprints_dag)
A configuração do airflow esta dentro da ec2, e o container rodando, um container com airflow e um container com o postgresql.
Para armazenar os dados estou usando o postgres.
O código da dag esta em [data_sprints_dag](./data_sprints_dag)

## QuickSight

[Dashboard](./quicksight/README.md) (prints).

## Analise

[Analise_Dados](./analise/Analise_Dados.ipynb)