from flask import request
import logging


#Funcao para coletar ip das requisicoes. 
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        ip = request.remote_addr
    return ip


# Funcao para Logging da aplicacao.
def setup_logging(log_file='logs/app.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger()
    return logger
