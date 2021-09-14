import sqlite3
from flask import Blueprint ,request

router = Blueprint("update-user", __name__) 

# 유저목록 변경
@router.route("/", methods=['PUT'])
def putUpdateUserRouter():
    try: 
        userName = request.form['name']
        userEmail = request.form['email']
        newName = request.form['newName']
        newEmail = request.form['newEmail']

        conn = sqlite3.connect('mydb.db')
        cur = conn.cursor()
        query = """UPDATE users SET name='%s', email='%s'
    WHERE name='%s' AND email='%s'""" % (newName, newEmail, userName, userEmail)
        cur.execute(query)
        print(cur.rowcount)
        if cur.rowcount > 0:
            conn.commit()
            conn.close()
            return {
                'status': 'success',
            }
        else:
            return {
                'status': 'fail',
                'msg' : 'sql이 적용되지 않았습니다. name과 email의 값이 db에 존재하는 값인지 확인해주세요.'
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