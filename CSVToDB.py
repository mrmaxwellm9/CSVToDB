import sqlite3
import os
from PyQt5.QtWidgets import *
from PyQt5 import *

# To DO
# ------------

#  3) Add error handling
#  5) Add progress bar
#  7) Make csv file name default table/db name

#  8) Make script to install dependencies
#  9) Make executable

#  1) Fix types (checking column name type right now not the data)

# Remove failed files

# Import less


class DialogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.setWindowModality(QtCore.Qt.ApplicationModal)


class MainWindow(QMainWindow):
    # Initialize the application GUI
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Enter")
        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setText("Select File")

        self.table_text = QLineEdit(self)
        self.db_text = QLineEdit(self)
        self.file_finder_text = QLineEdit(self)

        self.table_label = QtWidgets.QLabel(self)
        self.db_label = QtWidgets.QLabel(self)
        self.file_finder_label = QtWidgets.QLabel(self)

        self.table_label.setText('Table Name: ')
        self.db_label.setText('Database: ')
        self.file_finder_label.setText('File: ')

        self.setFixedHeight(360)
        self.setFixedWidth(640)

        self.table_label.move(200, 60)
        self.table_text.move(280, 60)
        self.db_label.move(200, 120)
        self.db_text.move(280, 120)
        self.file_finder_label.move(200, 180)
        self.file_finder_text.move(280, 180)
        self.file_button.move(400, 180)
        self.button1.move(280, 255)

        self.button1.clicked.connect(self.enter_button_clicked)
        self.file_button.clicked.connect(self.file_finder)

    # When the enter button is clicked
    def enter_button_clicked(self):
        if QtCore.Qt.MouseButton.LeftButton:
            # Open CSV file and set the database columns
            file_name = os.path.basename(self.file_finder_text.text())
            file_name = os.path.splitext(file_name)[0]
            try:
                csv_file = open(self.file_finder_text.text())
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Invalid CSV file')
                msg.setWindowTitle("Error")
                msg.exec_()
                return

            if self.table_text.text() == "":
                self.table_text.setText(file_name)
            if self.db_text.text() == "":
                self.db_text.setText(file_name)
            try:
                conn = sqlite3.connect((self.db_text.text()+'.db'))
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Invalid Database Name')
                msg.setWindowTitle("Error")
                msg.exec_()
                return
            cursor = conn.cursor()

            header = csv_file.readline().split(",")
            header[-1] = header[-1][:-1]

            sql_header_line = 'CREATE TABLE ' + self.table_text.text() + '('
            for column in header:
                column = column.replace(" ", "")
                if column.isnumeric():
                    sql_header_line += column + " int, "
                else:
                    sql_header_line += column + " nvarchar(255), "
            sql_header_line = sql_header_line[:-2] + ")"
            print(sql_header_line)
            cursor.execute(sql_header_line)
            conn.commit()

            # Insert the table contents
            header = [i.replace(" ", "") for i in header]
            contents = csv_file.readlines()[0:]
            for content in contents:
                content = content[:-1]
                content = tuple(content.split(","))
                sql_insert_line = "INSERT INTO " + \
                    self.table_text.text() + " VALUES (?"
                for i in range(len(header)-1):
                    sql_insert_line += ", ?"
                sql_insert_line += ")"
                cursor.execute(sql_insert_line, content)
                conn.commit()
            csv_file.close()

    # Execute the file finder when the button is pressed
    def file_finder(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.rootPath(), '*.csv')
        self.file_finder_text.setText(file_name)


# Run the app
def runApp():
    connector_app = QApplication([])
    window = MainWindow()
    window.show()
    connector_app.exec()


runApp()
