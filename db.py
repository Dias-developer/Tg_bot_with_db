import sqlite3

### Основные функций
# Create Table
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

# Add
def add_clients(username, phone_num, email):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute('INSERT INTO clients (username, phone_number, email) VALUES (?, ?, ?)', (username, phone_num, email))

    db.commit()

    db.close()

# Show
def show_clients():
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute('SELECT * FROM clients')
    clients = c.fetchall()

    db.close()

    return clients

# Delete
def delete_client_by_id(client_id):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute(
        'DELETE FROM clients WHERE id = ?',
        (client_id,)
    )

    db.commit()
    db.close()

# Update
def update_client_by_id_username(client_id, username):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute(
        'UPDATE clients SET username = ? WHERE id = ?',
        (username, client_id)
    )

    db.commit()

    updated = c.rowcount

    db.close()

    return updated

### Utils
def client_exists(client_id):
    db = sqlite3.connect('database/clients.db')
    c = db.cursor()

    c.execute(
        'SELECT id FROM clients WHERE id = ?',
        (client_id,)
    )

    client = c.fetchone()

    db.close()

    return client is not None