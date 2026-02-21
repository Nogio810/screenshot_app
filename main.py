import sys
from PyQt6 import QtWidgets
from gui.main_window import MainWindow  # あなたのMainWindowがある場所

def main():
    app = QtWidgets.QApplication(sys.argv)  # アプリ本体を作る
    window = MainWindow()                   # ウィンドウを作る
    window.show()                           # 表示する
    sys.exit(app.exec())                    # イベントループ開始

if __name__ == "__main__":
    main()
