import sqlite3
from flask import Blueprint ,request
router = Blueprint("add-user", __name__)

# 유저목록 추가 
@router.route("/", methods=['POST'])
def postAddUserRouter():
    try:
        userName = request.form['name']
        userEmail = request.form['email']
        conn = sqlite3.connect('mydb.db')
        cur = conn.cursor()
        query = """INSERT INTO users(name, email) VALUES ('%s', '%s') 
""" % (userName, userEmail)
        cur.execute(query)
        conn.commit()
        conn.close()
        return {
            'status': 'success',
        }
    except sqlite3.Error as error:
        errorMssage = ' '.join(error.args)
        print(errorMssage)
        if errorMssage == 'UNIQUE constraint failed: users.email':
            return {
                'status': 'fail',
                'msg': "[SQLite error] : 이미 등록된 email이 있습니다. 새로운 이메일로 등록해주세요."
            }
        else:
            return {
                'status': 'fail',
                'msg': "[SQLite error] : " + errorMssage
            }
    except:
        return {
            'status': 'fail',
            'msg': '[Unexpected error] : 에러 발생',
        }