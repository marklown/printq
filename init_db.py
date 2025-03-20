import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO jobs (job, color, submitted_by) VALUES (?, ?, ?)",
            ('https://www.thingiverse.com/thing:6953122', 'black matte PLA', 'Mark')
)

connection.commit()
connection.close()