import sqlite3

conn = sqlite3.connect('appdetect.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Insert some safe apps
cursor.execute("INSERT INTO apps (name) VALUES ('whatsapp')")
cursor.execute("INSERT INTO apps (name) VALUES ('instagram')")
cursor.execute("INSERT INTO apps (name) VALUES ('telegram')")
cursor.execute("INSERT INTO apps (name) VALUES ('google pay')")

conn.commit()
conn.close()

print("Database created successfully!")