import sqlite3
from datetime import datetime, timedelta

banco = 'app.db'

def init_db():
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alert (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            user TEXT,
            description TEXT,
            timestamp DATE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ioc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER,
            type TEXT,
            data TEXT,
            FOREIGN KEY (alert_id) REFERENCES alert (id)
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        ''')
    conn.commit()
    conn.close()


def create_user(username, password_hash):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, password_hash FROM user WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user




def create_alert(source, user, description, iocs, timestamp):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alert (source, user, description, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (source, user, description, timestamp))
    alert_id = cursor.lastrowid

    for ioc in iocs:
        cursor.execute('''
            INSERT INTO ioc (alert_id, type, data)
            VALUES (?, ?, ?)
        ''', (alert_id, ioc['type'], ioc['data']))

    conn.commit()
    conn.close()
    return alert_id


def get_alerts(user=None, ioc_type=None, ioc_data=None, days=None):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    query = 'SELECT * FROM alert'
    params = []
    conditions = []

    # Query para pesquisar por users
    if user:
        conditions.append('user = ?')
        params.append(user)

    # Query para pesquisar por days
    if days:
        days_ago = datetime.now() - timedelta(days=int(days))
        conditions.append('timestamp >= ?')
        params.append(days_ago.strftime('%Y-%m-%d %H:%M:%S'))

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, params)
    alerts = cursor.fetchall()
    results = []

    for alert in alerts:

        ioc_query = 'SELECT type, data FROM ioc WHERE alert_id = ?'
        ioc_params = [alert[0]]

        # Query para pesquisar por Type of IOCs
        if ioc_type:
            ioc_query += ' AND type = ?'
            ioc_params.append(ioc_type)

        # Query para pesquisar por Data of IOCs
        if ioc_data:
            ioc_query += ' AND data = ?'
            ioc_params.append(ioc_data)

        cursor.execute(ioc_query, ioc_params)
        iocs = cursor.fetchall()
        if (ioc_type or ioc_data) and not iocs:
            continue

        results.append({
            "id": alert[0],
            "source:": alert[1],
            "description": alert[3],
            "iocs": [{"type": ioc[0], "data": ioc[1]} for ioc in iocs],
            "user": alert[2],
            "date": alert[4]
        })
    conn.close()
    return results


def get_alert_by_id(alert_id):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alert WHERE id = ?', (alert_id,))
    alert = cursor.fetchone()
    if alert:
        cursor.execute('SELECT type, data FROM ioc WHERE alert_id = ?', (alert_id,))
        iocs = cursor.fetchall()
        result = {
            "id": alert[0],
            "source": alert[1],
            "description": alert[3],
            "iocs": [{"type": ioc[0], "data": ioc[1]} for ioc in iocs],
            "user": alert[2],
            "date": alert[4]
        }
        conn.close()
        return result
    conn.close()
    return None


def ioc_exists(source, ioc_type, ioc_data):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT alert.id FROM alert
        JOIN ioc ON alert.id = ioc.alert_id
        WHERE alert.source = ? AND ioc.type = ? AND ioc.data = ?
    ''', (source, ioc_type, ioc_data))
    result = cursor.fetchone()
    conn.close()
    return result is not None
