from flask import Blueprint, request
import requests
import json
import sqlite3
import multiprocessing

router = Blueprint("send-mails-to-all", __name__)


apiUrlV1 = 'http://python.recruit.herrencorp.com/api/v1/mail'
apiUrlV2 = 'http://python.recruit.herrencorp.com/api/v2/mail'


headersV1 = {'Authorization': 'herren-recruit-python',
             'Content-Type': 'application/x-www-form-urlencoded'}
headersV2 = {'Authorization': 'herren-recruit-python',
             'Content-Type': 'application/json'}


@router.route("/", methods=['POST'])
def postSendMailsRouter():
    try:
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

        processes = []
        for mail in mails:
            if 'gamil.com' in mail['mailto'] or 'naver.com' in mail['mailto']:
                process = multiprocessing.Process(
                    target=sendMail, args=(headersV2, json.dumps(mail), apiUrlV2))
            else:
                process = multiprocessing.Process(
                    target=sendMail, args=(headersV1, mail, apiUrlV1))
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


def sendMail(headers, mail, apiUrl):
    while True:
        response = requests.post(apiUrl, data=mail, headers=headers)
        result = json.loads(response.text)
        if result['status'] == 'success':
            return True
