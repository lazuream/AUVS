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

        #异常栏设置为空(第0页)
        self.ui.success_error_Type.setCurrentIndex(0)

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

        #注册
        self.ui.pushButton_R_Sure.clicked.connect(lambda :self.register())

        #网址跳转功能
        self.goWeb()

        #显示登录界面
        self.show()


    def goWeb(self):
        self.ui.pushButton_GoBilibili.clicked.connect(lambda : webbrowser.open("https://www.bilibili.com/"))
        self.ui.pushButton_GoGitHub.clicked.connect(lambda: webbrowser.open("https://github.com/lazuream"))

    def login(self):
        # 异常栏设置为空(第0页)
        self.ui.success_error_Type.setCurrentIndex(0)

        # 获取用户输入的用户名和密码
        userName = self.ui.lineEdit_L_UserName.text()
        password = self.ui.lineEdit_L_Password.text()

        # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='auv_user_data')
        cursor = db.cursor()

        # 查询所有用户数据
        cursor.execute("SELECT * FROM user_data")
        rows = cursor.fetchall()

        # 遍历查询结果，存储用户名、密码和等级
        username_list = [row[0] for row in rows]
        password_list = [row[1] for row in rows]
        grade_list = [row[2] for row in rows]

        # 关闭数据库连接（建议在使用完毕后立即关闭）
        db.close()

        # 验证用户名和密码，如果匹配并且等级为3，则显示成功并打开主窗口
        for i in range(len(username_list)):
            if userName == username_list[i] and password == password_list[i]:
                if grade_list[i] == 3:
                    self.ui.success_error_Type.setCurrentIndex(1)

                    # 创建主窗口实例
                    self.win = MainWindow()
                    # 显示主窗口
                    self.win.show()
                    # 关闭当前窗口（可选，取决于你的应用逻辑）
                    # self.close()
                    break  # 验证成功后退出循环
        else:
            # 如果没有找到匹配的用户，显示错误信息
            self.ui.success_error_Type.setCurrentIndex(3)

    def register(self):
        # 设置异常栏为空（第0页）
        self.ui.success_error_Type.setCurrentIndex(0)

        newUserName = self.ui.lineEdit_R_UserName.text()
        newPassword = self.ui.lineEdit_R_Password.text()
        passwordCheck = self.ui.lineEdit_R_CheckPassWord.text()

        # 检查用户名和密码长度
        if len(newUserName) > 20 or len(newPassword) > 20 or len(newUserName) == 0 or len(newPassword) == 0:
            self.ui.success_error_Type.setCurrentIndex(4)
            return

        # 检查用户名是否已存在
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='auv_user_data')
        cursor = db.cursor()

        cursor.execute("SELECT * FROM user_data WHERE user_name = %s", (newUserName,))
        existing_user = cursor.fetchone()

        db.close()

        if existing_user:
            self.ui.success_error_Type.setCurrentIndex(5)
            return

        # 检查两次输入的密码是否一致
        if newPassword != passwordCheck:
            self.ui.success_error_Type.setCurrentIndex(6)
            return

        # 注册新用户
        db = pymysql.connect(host="localhost", user="root", password='123456', port=3306, db='auv_user_data')
        cursor = db.cursor()

        sql = "INSERT INTO user_data(user_name, user_password) VALUES(%s, %s)"
        cursor.execute(sql, (newUserName, newPassword))

        db.commit()
        db.close()

        self.ui.success_error_Type.setCurrentIndex(2)  # 注册成功

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
