from LogInUi import *
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import sys


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

        #网址跳转功能
        self.goWeb()

        #显示登录界面
        self.show()


    def goWeb(self):
        self.ui.pushButton_GoBilibili.clicked.connect(lambda : webbrowser.open("https://www.bilibili.com/"))
        self.ui.pushButton_GoGitHub.clicked.connect(lambda: webbrowser.open("https://github.com/lazuream"))


if __name__ == '__main__':
    #解决自适应缩放
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = LogInWindow()
    sys.exit(app.exec_())
