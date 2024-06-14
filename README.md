# API Challenge

## Descrição

Este projeto faz parte de um desafio. Trata-se de uma API desenvolvida em Flask que permite gerenciar alertas de segurança, incluindo a criação, listagem e detalhes de alertas. A API utiliza autenticação JWT para proteger os endpoints e armazena os dados em um banco de dados SQLite.

## Estrutura do Projeto

```
/api_challenge/
├── Dockerfile
├── README.md
├── app
│   ├── app.db
│   ├── app.py
│   ├── auth.py
│   ├── table.py
│   └── utils.py
├── docker-compose.yml
├── logs
└── requirements.txt
```


- `app.py`: Arquivo principal da aplicação Flask.
- `auth.py`: Módulo para lidar com autenticação JWT.
- `table.py`: Módulo para manipulação de dados no banco de dados.
- `utils.py`: Funções utilitárias, incluindo configuração de log e obtenção do IP das requests.
- `Dockerfile`: Arquivo para criação da imagem Docker.
- `docker-compose.yml`: Arquivo para configuração e execução dos contêineres Docker.
- `requirements.txt`: Lista de dependências do projeto.

## Instalação

### Pré-requisitos

- Docker
- Docker Compose

### Clonando o Repositório

```sh
git clone git@github.com:lailtonmontenegro/api_challenge.git
cd api_challenge
```
### Construção e Execução com Docker

```sh
docker-compose build
docker-compose up
```

Acessando o home.  
```shell
curl -X POST http://localhost:8080
```
Resposta
```json
{"title": "Lailton Api challenge"}
```

## Uso
### Autenticação
- Antes de usar a API, você precisa registrar um usuário e obter um token.
```sh
curl -X POST http://localhost:8080/auth/register -H "Content-Type: application/json" -d '{
    "username": "alice",
    "password": "password1"
}'
```
### Obter um Token

```shell
curl -X POST http://localhost:8080/auth/login -u alice:password1
```
### Usar o Token para Autenticação
- Adicione o token JWT no header Authorization para autenticar as requisições.