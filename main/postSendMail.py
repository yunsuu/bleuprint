from flask import Blueprint, request
import requests
import json

router = Blueprint("send-mail", __name__)


apiUrlV1 = 'http://python.recruit.herrencorp.com/api/v1/mail'
apiUrlV2 = 'http://python.recruit.herrencorp.com/api/v2/mail'


headersV1 = {'Authorization': 'herren-recruit-python',
             'Content-Type': 'application/x-www-form-urlencoded'}
headersV2 = {'Authorization': 'herren-recruit-python',
             'Content-Type': 'application/json'}

# 한개 이메일 보내기


@router.route("/", methods=['POST'])
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
            response = sendMail(headersV2, json.dumps(mail), apiUrlV2)
        else:
            response = sendMail(headersV1, mail, apiUrlV1)
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


def sendMail(headers, mail, apiUrl):
    while True:
        response = requests.post(apiUrl, data=mail, headers=headers)
        result = json.loads(response.text)
        if result['status'] == 'success':
            return True
