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
    "username": "alice",
    "password": "password1"
}'
```
### Obter um Token
```shell
curl -X POST http://localhost:8080/auth/login -u alice:password1
```

### Exemplo usando um Token para Autenticação

```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alert/10"
```

## Documentação da API
Esta api conta com 4 endpoins, abaixo maiores detalhes sobre cada um deles.
* /auth/registrer
* /auth/login 
* /alert  
* /alerts 


| Method | URL                         | Description                                | Response Codes                             |
|--------|-----------------------------|--------------------------------------------|--------------------------------------------|
| POST   | /auth/register              | Registra um novo usuário                   | 201 (Created), 400 (Bad Request)           |
| POST   | /auth/login                 | Autentica um usuário e retorna um token JWT| 200 (OK), 401 (Unauthorized)               |
| POST   | /alert                      | Cria um novo alerta                        | 201 (Created), 400 (Bad Request)           |
| GET    | /alerts                     | Lista todos os alertas                     | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?user={user}         | Filtra alertas por usuário                 | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?ioc_type={ioc_type} | Filtra alertas por tipo de IOC             | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?ioc_data={ioc_data} | Filtra alertas por dados de IOC            | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alerts?days={days}         | Filtra alertas dos últimos N dias          | 200 (OK), 404 (Not Found), 400 (Bad Request) |
| GET    | /alert/{id}                 | Obtém detalhes de um alerta específico     | 200 (OK), 404 (Not Found)                  |

## Exemplos de Uso

### Criar um Novo Alerta [ POST /alert ]

```shell
curl -H "Authorization: Bearer your_token" -X POST http://localhost:8080/alert -H "Content-Type: application/json" -d '{
    "source": "suricata",
    "user": "Alice",
    "description": "Known malware hash",
    "iocs": [{"type": "hash_md5", "data": "f0e3557d84a78cb1774d4402c85742c8"}],
    "date": "2024-06-12 12:00:00"
}'
```

### Listar Alertas [ GET /alerts ]
```shell
curl -H "Authorization: Bearer your_token" -X GET "http://localhost:8080/alerts"
```
- Você consegue filtrar especificando alguns parâmetros ou fazendo combinações entre elas. 
- Parâmetros. [ _ioc_type_, ], [_ioc_data_ ], [ _user_ ] e [ _days_ ].

1. Buscando por ioc_type. 
```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alerts?ioc_type=ip"
```
2. Buscando por ioc_data.
```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alerts?ioc_data=200.123.122.124"
```
3. Buscando por User. 
```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alerts?user=lailton"
```
4. Buscando por dias atrás utilizando days=N.
```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alerts?days=2"
```
É possível fazer combinações dos parâmetros. 

1. ```...-X GET "http://localhost:8080/alerts?days=2&ioc_type=Domain"```
2. ```...-X GET "http://localhost:8080/alerts?days=2&ioc_type=Domain&user=lailton"```

### Buscar por um alerta específico. 

```shell
curl -H "Authorization: Bearer $token" -X GET "http://localhost:8080/alert/26"
```

### Extras
* Este projeto conta com um arquivo de Log com detalhes das requisições, código de respostas e armazenamento do ip da requisição. 
Arquivo localicado no caminho `api_challenge/logs/app.log` 
* Não é possível importar o mesmo IOC se o source for o mesmo.
* É possível implementar o vários Ioc_Type para o mesmo alerta, conforme exemplo abaixo.
```json
{
    "id": 2,
    "source": "antivirus",
    "user": "security_team",
    "description": "Malware detected on endpoint",
    "iocs": [
        {"type": "hash_sha256", "data": "5d41402abc4b2a76b9719d911017c592"},
        {"type": "file_name", "data": "malware.exe"},
        {"type": "ip", "data": "198.51.100.1"}
    ],
    "date": "2024-06-12 12:00:00"
}
```

### Projeto by

Lailton Montenegro 




