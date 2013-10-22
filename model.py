# ADMIN_USER="hackbright"
# ADMIN_PASSWORD = 5980025637247534551
import sqlite3

DB = None
CONN = None

def authenticate(username, password):
    connect_to_db()
    query = """SELECT id FROM Users WHERE username = ? and password = ?"""
    DB.execute(query, (username, hash(password),))
    row = DB.fetchone()
    CONN.close()
    if row[0]:
        return row[0]
    else:
        return None

def get_user_by_name(username):
    connect_to_db()
    query = """SELECT id FROM Users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    CONN.close()
    if row:
        return row[0]
    else:
        return None

def get_name_by_id(user_id):
    connect_to_db()
    query = """SELECT username FROM Users WHERE id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    CONN.close()
    if row:
        return row[0]
    else:
        return None

def get_wall_posts_by_id(user_id):
    connect_to_db()
    query = """SELECT * from wall_posts where owner_id = ?"""
    # id, owner_id, author_id, created_at, content
    DB.execute(query, (user_id,))
    rows = DB.fetchall()
    CONN.close()
    if rows:
        return rows
    else:
        return None

def make_wall_post(owner_id, author_id, created_at, content):
    connect_to_db()
    query = """INSERT into wall_posts (owner_id, author_id, created_at, content) values(?, ?, ?, ?)"""
    DB.execute(query, (owner_id, author_id, created_at, content,))
    CONN.commit()
    CONN.close()

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()


def main():
    connect_to_db()
    CONN.close()

if __name__ == "__main__":
    main()