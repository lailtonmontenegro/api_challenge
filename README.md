# API Challenge

## Descrição

Este projeto é parte de um desafio para criar uma API que permite receber e gerenciar alertas de segurança, incluindo a criação, listagem e visualização detalhada de alertas. A API utiliza autenticação JWT para proteger seus endpoints.


## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask.
- `auth.py`: Módulo para lidar com autenticação JWT.
- `table.py`: Módulo para manipulação de dados no banco de dados.
- `utils.py`: Funções utilitárias, incluindo configuração de logging e obtenção do IP do cliente.
- `Dockerfile`: Arquivo para criação da imagem Docker.
- `docker-compose.yml`: Arquivo para configuração e execução dos contêineres Docker.
- `requirements.txt`: Lista de dependências do projeto.
 

## Instalação

### Pré-requisitos

- Docker
- Docker Compose

### Clonando o Repositório

```sh
git clone https://github.com/lailtonmontenegro/api_challenge.git
cd api_challenge
```

### Construção e Execução com Docker

Crie um arquivo .env para definir a chave secreta:
```shell
SECRET_KEY=$(python3 -c 'import os; print(os.urandom(24).hex())')
```

###### Obs: Lembre-se de executar o Docker com um usuário que tenha as permissões adequadas. 
```shell
docker-compose build
docker-compose up
```
Valide a aplicação. 
```shell
curl --request GET  \
     --url 'http://localhost:8080'
```
Resposta esperada

```json
{"title":"Api challenge - Lailton Montenegro"}
```

## Uso

### Autenticação
Antes de usar a API, você precisa registrar um usuário e obter um token.

### Registrar um Novo Usuário
```shell
curl -X POST http://localhost:8080/auth/register -H "Content-Type: application/json" -d '{
    "username": "lailton",
    "password": "password1"
}'
```
Resposta esperada

```json
{"message":"User created successfully"}
```

### Token
Para acessar a API você precisa obter um token de autenticação, 
para depois conseguir os resursos disponíveis através dos endpoints de API.

A API  espera que tenha um cabeçalho `Authorization` com o token obtido nesse passo, do tipo Bearer.

Da seguinte maneira:

`Authorization: Bearer <your-token>`

Request
POST - http://localhost:8080/auth/login

```shell
curl -X POST 'http://localhost:8080/auth/login' \
  -u lailton:password1 \
  -H "Content-Type: application/json"
```
O retorno será algo como:
```json
{
  "token": "<your-token>"
}
```

### Exemplo usando um Token para Autenticação

```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alert/10"
```


## Documentação da API
Esta api conta com 5 endpoins, abaixo maiores detalhes sobre cada um deles.
* /auth/registrer
* /auth/login 
* /alert  
* /alerts 
* /


| Method | URL                         | Description                                  | Response Codes                               |
|--------|-----------------------------|----------------------------------------------|----------------------------------------------|
| POST   | /auth/register              | Registra um novo usuário                     | 201 (Created), 400 (Bad Request)             |
| POST   | /auth/login                 | Autentica um usuário e retorna um token JWT  | 200 (OK), 401 (Unauthorized)                 |
| POST   | /alert                      | Cria um novo alerta                          | 201 (Created), 400 (Bad Request)             |
| GET    | /alerts                     | Lista todos os alertas                       | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?user={user}         | Filtra alertas por usuário                   | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?ioc_type={ioc_type} | Filtra alertas por tipo de IOC               | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?ioc_data={ioc_data} | Filtra alertas por dados de IOC              | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?days={days}         | Filtra alertas dos últimos N dias            | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alert/{id}                 | Obtém detalhes de um alerta específico       | 200 (OK), 404 (Not Found)                    |
| GET    | /                           | Endpoint inicial que retorna uma msg simples | 200 (OK)                                     |

## Exemplos de Uso

### Criar um Novo Alerta [ POST /alert ]

```shell
curl -H "Authorization: Bearer your_token" -X POST http://localhost:8080/alert -H "Content-Type: application/json" -d '{
    "source": "suricata",
    "user": "lailton",
    "description": "Known malware hash",
    "iocs": [{"type": "hash_md5", "data": "f0e3557d84a78cb1774d4402c85742c8"}],
    "date": "2024-06-12 12:00:00"
}'
```
Respostas esperadas


`201`
```json
{"id":1,"status":"Alert received successfully"}
```
`400`
```json
{"error 400":"Duplicate IOC for the same Source"}
```
```json
{"error 400":"Invalid input, missing date"}
```


## Listar Alertas [ GET /alerts ]
```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alerts"
```
- Você consegue filtrar especificando alguns parâmetros ou fazendo combinações entre elas. 
- Parâmetros. [ _ioc_type_, ], [_ioc_data_ ], [ _user_ ] e [ _days_ ].

1. Buscando por ioc_type. 
```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alerts?ioc_type=hash_md5"
```
2. Buscando por ioc_data.
```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alerts?ioc_data=f0e3557d84a78cb1774d4402c85742c8"
```
3. Buscando por User. 
```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alerts?user=lailton"
```
4. Buscando por dias atrás utilizando days=N.
```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alerts?days=2"
```
É possível fazer combinações dos parâmetros. 

1. ```...-X GET "http://localhost:8080/alerts?days=2&ioc_type=hash_md5"```
2. ```...-X GET "http://localhost:8080/alerts?days=2&ioc_type=hash_md5&user=lailton"```

Respostas esperadas

`200` (OK)   
`404`
```json
{"error 404":"No alerts found for the specified criteria"}
```
`400`
```json
{"error 400":"Invalid parameter: oc-type"}
```


## Buscar por um alerta específico. [ GET /alert ]

```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alert/26"
```
Respostas esperadas

`200` (OK)  
`404`
```json
{"error":"Alert not found"}
```

### Extras
* Este projeto conta com um arquivo de Log com detalhes das requisições, código de respostas e armazenamento do ip da requisição. 
Arquivo localicado no caminho `api_challenge/logs/app.log` 
* Não é possível importar o mesmo IOC se o source for o mesmo.
* É possível implementar vários Ioc_Type para o mesmo alerta, conforme exemplo abaixo.

```shell
curl -H "Authorization: Bearer $your_token" -X POST http://localhost:8080/alert \
  -H "Content-Type: application/json" \
  -d '{
    "source": "antivirus",
    "user": "security_team",
    "description": "Malware detected on endpoint",
    "iocs": [
        {"type": "hash_sha256", "data": "5d41402abc4b2a76b9719d911017c592"},
        {"type": "file_name", "data": "malware.exe"},
        {"type": "ip", "data": "198.51.100.1"}
    ],
    "date": "2024-06-12 12:00:00"
}'
```

. 

Lailton Montenegro 




