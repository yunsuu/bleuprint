from flask import Flask, request, Blueprint
import requests
import json
import multiprocessing
import sqlite3
from . import getUserList
from . import postAddUser


app = Flask(__name__)
app.register_blueprint(getUserList.router, url_prefix="/user-list") 
app.register_blueprint(postAddUser.router, url_prefix="/add-user") 


# app.register_blueprint(getUserList.getUserListRouter, url_prefix="/api")

apiUrl = 'http://python.recruit.herrencorp.com/api/v1/mail'
apiUrl2 = 'http://python.recruit.herrencorp.com/api/v2/mail'


headers = {'Authorization': 'herren-recruit-python',
           'Content-Type': 'application/x-www-form-urlencoded'}
headers2 = {'Authorization': 'herren-recruit-python',
            'Content-Type': 'application/json'}


def sendMail(headers, mail, apiUrl):
    while True:
        response = requests.post(apiUrl, data=mail, headers=headers)
        result = json.loads(response.text)
        print(result['status'])
        if result['status'] == 'success':
            return True

@app.route("/")
def getRootRouter():
    return "<p>서버가 정상적으로 켜졌습니다!</p>"



# 유저목록 변경
@app.route("/update-user", methods=['PUT'])
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

    

# 유저목록 삭제


@app.route("/delete-user", methods=['DELETE'])
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

# 한개 이메일 보내기
# post


@app.route("/send-mail", methods=['POST'])
def postSendMailRouter():
    try:
        mailto = request.form['mailto']
        subject = request.form['subject']
        content = request.form['content']

        mail = {
            "mailto": mailto,
            "subject": subject,
            "content": content
        }
        
        if 'gamil.com' in mail['mailto'] or 'naver.com' in mail['mailto']:
            response = sendMail(headers2, json.dumps(mail), apiUrl2)
        else:
            response = sendMail(headers, mail, apiUrl)
        if response == True:
            return {
                'status': 'success',
            }
        else:
            return {
                'status': 'fail',
            }
    except:
        return {
            'status': 'fail',
        }

# 다중 이메일 보내기
# post


@app.route("/send-mails-to-all", methods=['POST'])
def postSendMailsRouter():
    subject = request.form['subject']
    content = request.form['content']

    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print(rows)
    conn.close()
    mails = []
    for row in rows:
        userEmail = row[2]
        mails.append({
            "mailto": userEmail,
            "subject": subject,
            "content": content
        })

    # response = sendMail(headers=headers, mails=data, apiUrl=apiUrl)

    try:
        processes = []
        for mail in mails:
            # process = multiprocessing.Process(target=sendMail, args=(headers, mail, apiUrl))
            # process = multiprocessing.Process(target=sendMail, args=(headers2, json.dumps(mail), apiUrl2))
            if 'gamil.com' in mail['mailto'] or 'naver.com' in mail['mailto']:
                process = multiprocessing.Process(
                    target=sendMail, args=(headers2, json.dumps(mail), apiUrl2))
                print(' 구글이나 네이버!')
            else:
                process = multiprocessing.Process(
                    target=sendMail, args=(headers, mail, apiUrl))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        return {
            'status': 'success',
        }
    except:
        return {
            'status': 'fail',
        }

