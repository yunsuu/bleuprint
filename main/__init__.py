from flask import Flask
from .routers import getUserList
from .routers import postAddUser
from .routers import putUpdateUser
from .routers import deleteUser
from .routers import postSendMail
from .routers import sendMailToAll

app = Flask(__name__)

app.register_blueprint(getUserList.router, url_prefix="/user-list")
app.register_blueprint(postAddUser.router, url_prefix="/add-user")
app.register_blueprint(putUpdateUser.router, url_prefix="/update-user")
app.register_blueprint(deleteUser.router, url_prefix="/delete-user")
app.register_blueprint(postSendMail.router, url_prefix="/send-mail")
app.register_blueprint(sendMailToAll.router, url_prefix="/send-mails-to-all")


@app.route("/")
def getRootRouter():
    return "<p>서버가 정상적으로 켜졌습니다!</p>"
