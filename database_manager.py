import sqlite3 as sql
import sanitise_verify as sv

def get_forums():
    val = 0
    posts = quickcon('get_all', 'forums', 'SELECT * FROM forums', (val))
    return posts

def insert_details(username, email, password):
    encode_password = sv.check_PSWRD(password)
    encrypted_password = sv.encrypt_PSWRD(encode_password)
    if sv.check_identical(encode_password, encrypted_password):
        quickcon("commit", 'user_info', 'INSERT INTO users (username,email,password) VALUES (?,?,?)', (username,email,encrypted_password))
        return True
    else:
        return "Password does not match"
    
def retrieve_details(email, password):
    encode_password = sv.check_PSWRD(password)
    details = quickcon("fetchone", 'user_info', 'SELECT password FROM users WHERE email=(?)', (email,))
    for detail in details:
        if sv.check_identical(encode_password, detail):
            return True
        else:
            return False
        
def update_session(email, secret_key):
    quickcon("commit", 'user_info', 'UPDATE users SET current_session=(?) WHERE email=(?)', (secret_key, email))

def reset_session(email):
    quickcon("commit", 'user_info', 'UPDATE users SET current_session=(?) WHERE email=(?)', ('signed out', email))

def check_session(email):
    session = quickcon("fetchone", 'user_info', 'SELECT current_session FROM users WHERE email=(?)', (email,))
    return session[0]


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
        val = cur.execute(f"{command}",).fetchall()
        con.close()
        return val