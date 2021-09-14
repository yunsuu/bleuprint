import sqlite3
from flask import Blueprint 
router = Blueprint("user-list", __name__) 

# 유저목록 조회
@router.route("/")
def getUserListRouter():
    try: 
        conn = sqlite3.connect('mydb.db')
        cur = conn.cursor()
        query = "SELECT * FROM users"
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        result = []
        print(rows)
        for row in rows:
            result.append({'name': row[1], 'email': row[2]})
        return {
            'status': 'success',
            'result': result,
        }
    except sqlite3.Error as error:
        errorMssage = ' '.join(error.args)
        print(errorMssage)
        return {
            'status': 'fail',
            'msg': '[SQLite error] :' + errorMssage,
        }
    except:
        return {
            'status': 'fail',
            'msg': '[Unexpected error] : 에러 발생',
        }