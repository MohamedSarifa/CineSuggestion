from database import cursor, conn

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    movie_name TEXT
)
""")

conn.commit()

print("Tables created successfully.")