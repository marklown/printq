import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN comments text")

connection.commit()
connection.close()
