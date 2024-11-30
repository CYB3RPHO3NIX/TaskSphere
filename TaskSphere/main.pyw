import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QListWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QDateTimeEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QFrame, QComboBox
)
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QColor
from plyer import notification  # For native notifications

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager Tool")
        self.setGeometry(100, 100, 1000, 600)
        self.main_layout = QHBoxLayout()

        # Navigation Panel
        self.nav_panel = QListWidget()
        self.nav_panel.addItems(["Tasks", "Reminders", "Credentials", "Notes", "Open Questions"])
        self.nav_panel.currentRowChanged.connect(self.display_section)
        self.main_layout.addWidget(self.nav_panel, 1)

        # Content Area
        self.content_area = QStackedWidget()
        self.main_layout.addWidget(self.content_area, 4)

        # Sections
        self.init_tasks_section()
        self.init_reminders_section()
        self.init_credentials_section()
        self.init_notes_section()
        self.init_open_questions_section()

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def init_tasks_section(self):
        """Tasks Section"""
        self.tasks_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tasks with Sub-tasks"))
        self.tasks_table = QTableWidget(0, 3)
        self.tasks_table.setHorizontalHeaderLabels(["Task", "Status", "Sub-tasks"])
        layout.addWidget(self.tasks_table)

        self.content_area.addWidget(self.tasks_widget)
        self.tasks_widget.setLayout(layout)

    def init_reminders_section(self):
        """Reminders Section"""
        self.reminders_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Reminders"))
        self.reminders_table = QTableWidget(0, 3)
        self.reminders_table.setHorizontalHeaderLabels(["Reminder", "Date & Time", "Actions"])
        layout.addWidget(self.reminders_table)

        # Add Reminder Inputs
        self.reminder_input = QLineEdit()
        self.reminder_datetime = QDateTimeEdit(QDateTime.currentDateTime())
        self.reminder_datetime.setCalendarPopup(True)
        add_reminder_btn = QPushButton("Add Reminder")
        add_reminder_btn.clicked.connect(self.add_reminder)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.reminder_input)
        input_layout.addWidget(self.reminder_datetime)
        input_layout.addWidget(add_reminder_btn)
        layout.addLayout(input_layout)

        self.content_area.addWidget(self.reminders_widget)
        self.reminders_widget.setLayout(layout)

        # Timer for checking reminders
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)  # Check every minute

    def add_reminder(self):
        text = self.reminder_input.text()
        date_time = self.reminder_datetime.dateTime().toString()
        if text:
            row_position = self.reminders_table.rowCount()
            self.reminders_table.insertRow(row_position)
            self.reminders_table.setItem(row_position, 0, QTableWidgetItem(text))
            self.reminders_table.setItem(row_position, 1, QTableWidgetItem(date_time))
            self.reminder_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a reminder.")

    def check_reminders(self):
        current_time = QDateTime.currentDateTime().toString()
        for row in range(self.reminders_table.rowCount()):
            reminder_time = self.reminders_table.item(row, 1).text()
            if reminder_time <= current_time:
                notification.notify(
                    title="Reminder",
                    message=self.reminders_table.item(row, 0).text(),
                    timeout=5
                )

    def init_credentials_section(self):
        """Credentials Section"""
        self.credentials_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Credentials"))
        self.credentials_table = QTableWidget(0, 4)
        self.credentials_table.setHorizontalHeaderLabels(["Username", "Hostname", "Password", "Copy"])
        layout.addWidget(self.credentials_table)

        self.content_area.addWidget(self.credentials_widget)
        self.credentials_widget.setLayout(layout)

    def init_notes_section(self):
        """Notes Section"""
        self.notes_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Notes"))
        self.notes_table = QTableWidget(0, 2)
        self.notes_table.setHorizontalHeaderLabels(["Section", "Notes"])
        layout.addWidget(self.notes_table)

        self.content_area.addWidget(self.notes_widget)
        self.notes_widget.setLayout(layout)

    def init_open_questions_section(self):
        """Open Questions Section"""
        self.questions_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Open Questions"))
        self.questions_table = QTableWidget(0, 3)
        self.questions_table.setHorizontalHeaderLabels(["Question", "Answer", "Status"])
        layout.addWidget(self.questions_table)

        self.content_area.addWidget(self.questions_widget)
        self.questions_widget.setLayout(layout)

    def display_section(self, index):
        self.content_area.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
