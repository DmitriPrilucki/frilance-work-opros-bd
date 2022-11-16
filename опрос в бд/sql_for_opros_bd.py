import sqlite3


db = sqlite3.connect('new2count.db')
cur = db.cursor()


async def db_conn():
    cur.execute("CREATE TABLE IF NOT EXISTS test (user_id INTEGER PRIMARY KEY, user_name TEXT, count INT DEFAULT 0)")

    db.commit()


async def new_user_name(user_name):
    cur.execute("INSERT INTO test (user_name) VALUES(?)", (user_name,))
    db.commit()


async def new_user(user_id):
    cur.execute("INSERT INTO test (user_id) VALUES(?)", (user_id,))
    db.commit()


async def update_count(user_id):
    cur.execute("UPDATE test SET count = count + 1 WHERE user_id = ?", (user_id,))
    db.commit()


async def sel_count(user_id):
    x = cur.execute("SELECT count FROM test WHERE user_id = ?", (user_id,)).fetchone()
    return x


async def zero_count(user_id):
    cur.execute("UPDATE test SET count = 0 WHERE user_id = ?", (user_id,)).fetchone()
    db.commit()