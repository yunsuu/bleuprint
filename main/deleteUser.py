import sqlite3
from flask import Blueprint, request

router = Blueprint("delete-user", __name__)

# 유저목록 삭제


@router.route("/", methods=['DELETE'])
def deleteUserRouter():
    try:
        userName = request.form['name']
        userEmail = request.form['email']

        conn = sqlite3.connect('mydb.db')
        cur = conn.cursor()

        query = "DELETE FROM users WHERE name='%s' AND email='%s'" % (
            userName, userEmail)
        cur.execute(query)
        print(cur.rowcount)
        if cur.rowcount > 0:
            conn.commit()
            conn.close()
            return {
                'status': 'success',
            }
        else:
            conn.close()
            return {
                'status': 'fail',
                'msg': 'sql이 적용되지 않았습니다. 이미 삭제되거나 등록되지 않은 유저 정보입니다.'
            }
    except sqlite3.Error as error:
        errorMssage = ' '.join(error.args)
        print(errorMssage)
        return {
            'status': 'fail',
            'msg': "[SQLite 에러] : " + errorMssage
        }
    except:
        return {
            'status': 'fail',
            'msg': '[예상불가 에러] : 에러 발생',
        }
