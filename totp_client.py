import sys
import json
import os
import time
import pyotp
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class TOTPManager:
    def __init__(self, storage_file='secrets.json'):
        self.storage_file = storage_file
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_accounts(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.accounts, f)
    
    def add_account(self, name, secret):
        secret = secret.replace(' ', '').upper()
        try:
            totp = pyotp.TOTP(secret)
            totp.now()
            self.accounts[name] = secret
            self.save_accounts()
            return True
        except:
            return False
    
    def remove_account(self, name):
        if name in self.accounts:
            del self.accounts[name]
            self.save_accounts()
            return True
        return False
    
    def get_code(self, name):
        if name in self.accounts:
            totp = pyotp.TOTP(self.accounts[name])
            return totp.now()
        return None
    
    def time_remaining(self):
        return 30 - (int(time.time()) % 30)

class AccountWidget(QWidget):
    delete_requested = pyqtSignal(str)
    
    def __init__(self, name, manager):
        super().__init__()
        self.name = name
        self.manager = manager
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Название аккаунта
        name_label = QLabel(self.name)
        name_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 500;
            color: #000000;
        """)
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # Код
        self.code_label = QLabel()
        self.code_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #000000;
            font-family: 'Consolas', 'Courier New', monospace;
            letter-spacing: 2px;
        """)
        layout.addWidget(self.code_label)
        
        # Кнопка копирования
        self.copy_btn = QPushButton("COPY")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: #ffffff;
                border: none;
                padding: 5px 15px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #333333;
            }
            QPushButton:pressed {
                background: #555555;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_code)
        layout.addWidget(self.copy_btn)
        
        # Кнопка удаления
        delete_btn = QPushButton("DELETE")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666666;
                border: 1px solid #666666;
                padding: 5px 15px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #000000;
                color: #ffffff;
                border-color: #000000;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.name))
        layout.addWidget(delete_btn)
        
        self.setLayout(layout)
        self.update_code()
    
    def update_code(self):
        code = self.manager.get_code(self.name)
        if code:
            formatted_code = f"{code[:3]} {code[3:]}"
            self.code_label.setText(formatted_code)
    
    def copy_code(self):
        code = self.manager.get_code(self.name)
        if code:
            QApplication.clipboard().setText(code)
            self.copy_btn.setText("COPIED")
            QTimer.singleShot(1000, lambda: self.copy_btn.setText("COPY"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = TOTPManager()
        self.account_widgets = {}
        self.init_ui()
        
        # Таймер для обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(100)
        
    def init_ui(self):
        self.setWindowTitle("TOTP Authenticator")
        self.setFixedSize(500, 700)
        
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Заголовок
        header = QWidget()
        header.setStyleSheet("background: #000000;")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(30, 30, 30, 20)
        
        title = QLabel("TOTP AUTHENTICATOR")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: white;
            letter-spacing: 2px;
        """)
        header_layout.addWidget(title)
        
        # Прогресс бар
        progress_container = QWidget()
        progress_container.setStyleSheet("background: transparent;")
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 10, 0, 0)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 30)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(2)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #333333;
                border: none;
            }
            QProgressBar::chunk {
                background: #ffffff;
            }
        """)
        progress_layout.addWidget(self.progress)
        
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            color: #999999;
            font-size: 11px;
            font-weight: 500;
            margin-top: 5px;
        """)
        progress_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        progress_container.setLayout(progress_layout)
        header_layout.addWidget(progress_container)
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: #e0e0e0; height: 1px;")
        main_layout.addWidget(line)
        
        # Область со списком аккаунтов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: #ffffff;
                border: none;
            }
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999999;
            }
        """)
        
        self.accounts_widget = QWidget()
        self.accounts_layout = QVBoxLayout()
        self.accounts_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.accounts_layout.setSpacing(0)
        self.accounts_layout.setContentsMargins(0, 0, 0, 0)
        self.accounts_widget.setLayout(self.accounts_layout)
        
        scroll.setWidget(self.accounts_widget)
        main_layout.addWidget(scroll)
        
        # Кнопка добавления
        add_btn = QPushButton("ADD ACCOUNT")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: white;
                border: none;
                padding: 20px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: #1a1a1a;
            }
            QPushButton:pressed {
                background: #333333;
            }
        """)
        add_btn.clicked.connect(self.add_account)
        main_layout.addWidget(add_btn)
        
        central.setLayout(main_layout)
        
        # Стиль приложения
        self.setStyleSheet("""
            QMainWindow {
                background: #ffffff;
            }
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            QMessageBox {
                background: #ffffff;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background: #000000;
                color: white;
                border: none;
                padding: 5px 20px;
                min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background: #333333;
            }
        """)
        
        # Загрузка существующих аккаунтов
        self.load_accounts()
    
    def load_accounts(self):
        for name in self.manager.accounts:
            self.add_account_widget(name)
    
    def add_account_widget(self, name):
        widget = AccountWidget(name, self.manager)
        widget.delete_requested.connect(self.delete_account)
        
        # Контейнер
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
            QWidget:hover {
                background: #fafafa;
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(widget)
        container.setLayout(container_layout)
        
        self.accounts_layout.addWidget(container)
        self.account_widgets[name] = widget
    
    def add_account(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Account")
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background: #ffffff;
            }
            QLabel {
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 5px;
            }
            QLineEdit {
                background: #ffffff;
                border: 2px solid #e0e0e0;
                padding: 10px;
                color: #000000;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
            }
            QPushButton {
                background: #000000;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #333333;
            }
            QCheckBox {
                color: #666666;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #cccccc;
                background: white;
            }
            QCheckBox::indicator:checked {
                background: #000000;
                border-color: #000000;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        name_label = QLabel("ACCOUNT NAME")
        layout.addWidget(name_label)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("e.g., GitHub")
        layout.addWidget(name_input)
        
        secret_label = QLabel("SECRET KEY")
        layout.addWidget(secret_label)
        
        secret_input = QLineEdit()
        secret_input.setPlaceholderText("e.g., JBSWY3DPEHPK3PXP")
        secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(secret_input)
        
        # Чекбокс для показа ключа
        show_secret = QCheckBox("Show secret key")
        show_secret.stateChanged.connect(
            lambda: secret_input.setEchoMode(
                QLineEdit.EchoMode.Normal if show_secret.isChecked() 
                else QLineEdit.EchoMode.Password
            )
        )
        layout.addWidget(show_secret)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666666;
                border: 2px solid #e0e0e0;
            }
            QPushButton:hover {
                border-color: #999999;
                color: #333333;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        buttons_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("ADD")
        ok_btn.clicked.connect(dialog.accept)
        buttons_layout.addWidget(ok_btn)
        
        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = name_input.text().strip()
            secret = secret_input.text().strip()
            
            if name and secret:
                if name in self.manager.accounts:
                    QMessageBox.warning(self, "Error", "Account already exists")
                elif self.manager.add_account(name, secret):
                    self.add_account_widget(name)
                else:
                    QMessageBox.warning(self, "Error", "Invalid secret key")
    
    def delete_account(self, name):
        reply = QMessageBox.question(
            self, "Delete Account",
            f"Delete account '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.remove_account(name)
            
            # Удаляем виджет
            for i in range(self.accounts_layout.count()):
                container = self.accounts_layout.itemAt(i).widget()
                if container and container.findChild(AccountWidget).name == name:
                    container.deleteLater()
                    break
            
            del self.account_widgets[name]
    
    def update_all(self):
        remaining = self.manager.time_remaining()
        self.progress.setValue(30 - remaining)
        self.time_label.setText(f"REFRESH IN {remaining}s")
        
        # Обновляем коды каждую секунду
        if int(time.time() * 10) % 10 == 0:
            for widget in self.account_widgets.values():
                widget.update_code()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Установка шрифта для Windows
    if sys.platform == "win32":
        font = QFont("Segoe UI", 9)
        app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()