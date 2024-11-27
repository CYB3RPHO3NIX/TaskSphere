
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the window
        self.setWindowTitle("PyQt5 Example")
        self.setGeometry(100, 100, 300, 200)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label
        self.label = QLabel("Click the button to see a message", self)
        layout.addWidget(self.label)

        # Create a button
        self.button = QPushButton("Click Me!", self)
        layout.addWidget(self.button)

        # Connect the button's click event to a method
        self.button.clicked.connect(self.on_button_click)

        # Set the layout for the window
        self.setLayout(layout)

    def on_button_click(self):
        # Update the label text when the button is clicked
        self.label.setText("Hello, PyQt5!")

# Main entry point
if __name__ == "__main__":
    # Create the application object
    app = QApplication(sys.argv)

    # Create an instance of the application window
    window = SimpleApp()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
