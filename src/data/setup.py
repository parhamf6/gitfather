import sqlite3 
conn = sqlite3.connect(r"C:\Users\ASUS\Desktop\Codes\Project\Python\the-gitfather\src\data\db.sqlite3")
cursor = conn.cursor()


# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    username TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Create settings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    start_hour INTEGER,
    end_hour INTEGER,
    custom_msg TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')



conn.commit()
conn.close()