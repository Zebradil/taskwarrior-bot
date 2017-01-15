import sqlite3

conn = sqlite3.connect('bot.db')
c = conn.cursor()

c.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY)')
