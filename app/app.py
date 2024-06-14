from flask import Flask, jsonify, request
import table
from utils import setup_logging, get_client_ip
from auth import auth_bp, token_required
import os

app = Flask(__name__)

# Carregar a chave secreta da variável de ambiente
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Configurar logging
logger = setup_logging()

# Inicializar a base de dados
table.init_db()

# Registrar blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth')


# Função para validar parâmetros de consultas do curl
def validate_query_params(params, allowed_params):
    for param in params:
        if param not in allowed_params:
            return False, param
    return True, None


# Endpoint para listar todos os alertas
@app.route('/alerts', methods=['GET'])
@token_required
def get_alerts(current_user):
    allowed_params = {'user', 'ioc_type', 'ioc_data', 'days'}
    is_valid, invalid_param = validate_query_params(request.args.keys(), allowed_params)
    if not is_valid:
        client_ip = get_client_ip()
        logger.error(f'GET /alerts - Invalid parameter: {invalid_param} - IP: {client_ip}')
        return jsonify({"error 400": f"Invalid parameter: {invalid_param}"}), 400

    user = request.args.get('user')
    ioc_type = request.args.get('ioc_type')
    ioc_data = request.args.get('ioc_data')
    days = request.args.get('days')
    alerts = table.get_alerts(user=user, ioc_type=ioc_type, ioc_data=ioc_data, days=days)
    client_ip = get_client_ip()
    logger.info(f'GET /alerts - Params: user={user}, ioc_type={ioc_type}, ioc_data={ioc_data}, days={days} - IP: {client_ip}')

    if not alerts:
        return jsonify({"error 404": "No alerts found for the specified criteria"}), 404

    return jsonify(alerts)


# Endpoint para obter detalhes de um alerta específico
@app.route('/alert/<int:id>', methods=['GET'])
@token_required
def get_alert(current_user, id):
    alert = table.get_alert_by_id(id)
    client_ip = get_client_ip()
    if alert is not None:
        logger.info(f'GET /alert/{id} - Found - IP: {client_ip}')
        return jsonify(alert)
    else:
        logger.warning(f'GET /alert/{id} - Not Found - IP: {client_ip}')
        return jsonify({"error": "Alert not found"}), 404


# Endpoint para adicionar um novo alerta
@app.route('/alert', methods=['POST'])
@token_required
def create_alert(current_user):
    required_fields = ['source', 'user', 'description', 'iocs', 'date']
    client_ip = get_client_ip()

    for field in required_fields:
        if field not in request.json:
            logger.error(f'POST /alert - Invalid input, missing {field} - IP: {client_ip}')
            return jsonify({"error 400": f"Invalid input, missing {field}"}), 400

    source = request.json.get('source', "")
    user = request.json.get('user', "")
    description = request.json.get('description', "")
    iocs = request.json.get('iocs', [])
    date = request.json.get('date', "")

    # Validate IOC structure
    if not isinstance(iocs, list) or any('type' not in ioc or 'data' not in ioc for ioc in iocs):
        logger.error(
            f'POST /alert - Invalid input, iocs must be a list of objects with "type" and "data" - IP: {client_ip}')
        return jsonify({"error 400": "Invalid input, iocs must be a list of objects with 'type' and 'data'"}), 400

    # Check for duplicate IOCs for the same Source
    for ioc in iocs:
        if table.ioc_exists(source, ioc['type'], ioc['data']):
            logger.error(f'POST /alert - Duplicate IOC for Source {source} - IP: {client_ip}')
            return jsonify({"error 400": "Duplicate IOC for the same Source"}), 400

    alert_id = table.create_alert(source, user, description, iocs, date)
    logger.info(f'POST /alert - Alert created with ID {alert_id} - IP: {client_ip}')

    response = {
        "id": alert_id,
        "status": "Alert received successfully"
    }
    return jsonify(response), 201


# Endpoint inicial
@app.route('/')
def home():
    client_ip = get_client_ip()
    logger.info(f'GET / - Home - IP: {client_ip}')
    return jsonify({"title": "Api challenge - Lailton Montenegro"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

