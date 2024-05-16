from LogInUi import *
from testUItwo import *
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import sys
import pymysql


class LogInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LogInWindow()
        self.ui.setupUi(self)

        # 不显示windows框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #阴影效果
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0,0)
        self.shadow.setBlurRadius(2)
        self.shadow.setColor(QtCore.Qt.black)

        #将阴影效果置入
        #self.ui.mainLogIn.setGraphicsEffect(self.shadow)

        # 窗口居中
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕大小
        self.top = int((screen.width() - self.width()) / 2)  # 左上角x坐标
        self.left = int((screen.height() - self.height()) / 2)  # 左上角y坐标
        self.setGeometry(self.top, self.left, self.width(), self.height())

        #切换登录和注册界面
        self.ui.pushButton_LogIn.clicked.connect(lambda: self.ui.stackedWidget_LR.setCurrentIndex(0))
        self.ui.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_LR.setCurrentIndex(1))

        #登录
        self.ui.pushButton_L_Sure.clicked.connect(lambda :self.login())

        #网址跳转功能
        self.goWeb()

        #显示登录界面
        self.show()


    def goWeb(self):
        self.ui.pushButton_GoBilibili.clicked.connect(lambda : webbrowser.open("https://www.bilibili.com/"))
        self.ui.pushButton_GoGitHub.clicked.connect(lambda: webbrowser.open("https://github.com/lazuream"))

    def login(self):
        userName = self.ui.lineEdit_L_UserName.text()
        passWord = self.ui.lineEdit_L_PassWord.text()
        username_list = []
        password_list=[]
        grade_list=[]
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='auv_user_data')
        cursor = db.cursor()
        cursor.execute("select * from user_data")
        rows = cursor.fetchall()
        for row in rows:
            username_list.append(row[0])
            password_list.append(row[1])
            grade_list.append(row[2])
        # print(username_list,password_list,grade_list)
        # print(rows)
        db.commit()
        db.close()
        for i in range(len(username_list)):
            if userName ==  username_list[i] and passWord == password_list[i]:
                if grade_list[i] == 3:
                    self.win = MainWindow()
                    self.close()
            else:
                print("wrong!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #不显示windows框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(5, 5)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtCore.Qt.black)
        #self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.show()

if __name__ == '__main__':
    #解决自适应缩放
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = LogInWindow()
    sys.exit(app.exec_())
