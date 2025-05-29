import sqlite3 as sql

def get_forums():
    val = 0
    posts = quickcon('get_all', 'forums', 'SELECT * FROM forums', (val))
    return posts

def quickcon(type, db, command, var):
    if type == 'fetchone':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        val = cur.execute(f"{command}",(var)).fetchone()
        con.close()
        return val
    elif type == 'fetchall':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        val = cur.execute(f"{command}",(var)).fetchall()
        con.close()
        return val
    elif type == 'commit':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        cur.execute(f"{command}",(var))
        con.commit()
        con.close()
    elif type == 'get_all':
        con = sql.connect(f".database/{db}.db")
        cur = con.cursor()
        val = cur.execute(f"{command}").fetchall()
        con.close()
        return val