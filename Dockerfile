# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os requisitos do projeto
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app/ .

# Definir a variável de ambiente para a chave secreta
# Como estamos em um ambiente de poc, vou gerar uma chave aleatorio sempre que buildar o contêiner
RUN python -c "import os; print(f'SECRET_KEY={os.urandom(24).hex()}')" > .env

# Expor a porta da aplicação
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["python", "app.py"]
