import os
import smtplib
import imghdr
from email.message import EmailMessage
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys



EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''

class PasswordWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        self.btn_login.clicked.connect(self.btn_loginClicked)
        self.btn_exit.clicked.connect(self.btn_exitClicked)
        # self.txt_username.clear()


    def btn_loginClicked(self):
        try:
            global EMAIL_ADDRESS
            global EMAIL_PASSWORD
            EMAIL_ADDRESS = self.txt_username.text()
            EMAIL_PASSWORD = self.txt_password.text()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                print('OK2')
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.quit()
            self.accept()
        except:
            QMessageBox.warning(self,'Hata', 'Hatalı e-posta ve şifre kombinasyonu')

    def btn_exitClicked(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('myMail.ui', self)
        self.setWindowTitle('Generic Window')
        self.btnSend.clicked.connect(self.btnSendClicked)
        self.btnQuit.clicked.connect(self.btnQuitClicked)
        self.btnAddDoc.clicked.connect(self.btnAddDocClicked)
        self.btnAddPhoto.clicked.connect(self.btnAddPhotoClicked)
        self.msg = EmailMessage()
        self.pathArr = []
        self.pathImg = []
        self.image_files = []

    def btnSendClicked(self):
        self.msg['Subject'] = self.txt_topic.text()
        self.msg['From'] = EMAIL_ADDRESS
        self.msg['To'] = self.txt_receiver.text()  # ', '.join(contacts)
        self.msg.set_content(self.txt_message.toPlainText())

        if len(self.pathArr):
            with open(self.pathArr[-1], 'rb') as f:
                file_data = f.read()
                file_name = f.name
                self.msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        if len(self.image_files):
            for file in self.image_files:
                with open(file, 'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                    file_name = f.name
                self.add_attachment(file_data, maintype='image', subtype=file_type, filename = file_name )


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(self.msg)
            self.pathArr.clear()
            smtp.quit()
            self.msg.clear()
            self.txt_topic.clear()
            self.txt_message.clear()
            self.txt_receiver.clear()

    def btnQuitClicked(self):
        self.close()

    def btnAddDocClicked(self, sender):
        path = QFileDialog.getOpenFileName(self, 'Bir dosya seçiniz', '.', 'Text Files(*.txt);;All Files(*.*)')
        if path[0] != '':
            self.pathArr = path[0].split('/')

    def btnAddPhotoClicked(self, sender):
        path = QFileDialog.getOpenFileName(self, 'Bir dosya seçiniz', '.', 'Image Files(*.jpg);;Image Files(*.png);;Image Files(*.jpeg);;All Files(*.*)')
        if path[0] != '':
            print(path)
            self.pathImg = path[0].split('/')
           

def main():
    app = QApplication(sys.argv)
    passwordWindow = PasswordWindow()

    if passwordWindow.exec_() == QDialog.Accepted:
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec_()


main()
















