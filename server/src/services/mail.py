from flask import Flask
from flask_mail import Mail, Message
from threading import Thread

class MailService:
    __sender: str = "masjid@sample.com"
    __mail: Mail
    __message: Message
    __app: Flask

    def configure(self, app: Flask):
        app.config['MAIL_SERVER']='smtp.mailtrap.io'
        app.config['MAIL_PORT'] = 2525
        app.config['MAIL_USERNAME'] = 'a6d93d2b08f16c'
        app.config['MAIL_PASSWORD'] = '7b592d452c7ab7'
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        self.__mail = Mail(app)
        self.__app = app
    
    def messageBody(self, titie, reciever, body):
        self.__message = Message(titie, sender=self.__sender, recipients=[reciever])
        self.__message.body = body
        return self
    
    def sendInThread(self, app, send_mail, message):
        with app.app_context():
            send_mail(message)
    
    def send(self):
        Thread(target=self.sendInThread, args=(self.__app, self.__mail.send, self.__message, )).start()

mailService = MailService()