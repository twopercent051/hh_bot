import sqlite3 as sq
import io
import time


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print('Datebase connected OK')
    base.execute("""
        CREATE TABLE IF NOT EXISTS requests(
        id INTEGER PRIMARY KEY, 
        user_id INTEGER, 
        nickname VARCHAR(50), 
        contact VARCHAR(300), 
        vac_id INTEGER, 
        reg_date INTEGER,
        status VARCHAR(15))
        """)
    base.commit()


def dumper():
    with io.open('backupdatabase.sql', 'w') as p:
        for line in base.iterdump():
            p.write('%s\n' % line)


async def create_request(user_id, username, contact, vac_id):
    reg_date = int(time.time())
    cur.execute('INSERT INTO requests (user_id, nickname, reg_date, contact, vac_id, status) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, username, reg_date, contact, vac_id, 'waiting'))
    base.commit()


async def get_requests(status):
    result = cur.execute('SELECT * FROM requests WHERE status = (?)', (status,)).fetchall()
    return result


async def update_status(new_status, req_id):
    cur.execute('UPDATE requests SET status = (?) WHERE id = (?)', (new_status, req_id))
    base.commit()