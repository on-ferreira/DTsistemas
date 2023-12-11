# Projeto DTsistemas - README

Aqui estão as instruções para configurar e executar o projeto em seu ambiente local.

## Requisitos

Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina antes de prosseguir.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuração do Ambiente

1. Clone este repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/on-ferreira/DTsistemas.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd DTsistemas
   ```

3. Execute o seguinte comando para iniciar os containers do Docker:

   ```bash
    docker-compose up --build
   ```

Este comando irá construir as imagens necessárias e iniciar dois containers: um para o PostgreSQL (banco de dados) e outro para o próprio projeto XYZ.

## Acesso ao Projeto:

Após a conclusão do processo de inicialização, você pode acessar o projeto em http://localhost:5095 no seu navegador.
