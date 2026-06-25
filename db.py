import sqlite3

### Основные функций
def create_table():
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute(''' CREATE TABLE IF NOT EXISTS clients (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  phone_number TEXT,
                  email TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    db.commit()
    db.close()

def add_clients(username, phone_num, email):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute('INSERT INTO clients (username, phone_number, email) VALUES (?, ?, ?)', (username, phone_num, email))

    db.commit()

    db.close()

def show_clients():
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute('SELECT * FROM clients')
    clients = c.fetchall()

    db.close()

    return clients

def delete_client_by_id(client_id):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute(
        'DELETE FROM clients WHERE id = ?',
        (client_id,)
    )

    db.commit()
    db.close()