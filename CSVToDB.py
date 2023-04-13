from sqlite3 import connect
from os import path
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QLineEdit, QLabel, QMessageBox, QFileDialog, QApplication, QMainWindow
from PyQt5 import QtCore


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
        self.button1 = QPushButton(self)
        self.button1.setText("Enter")
        self.file_button = QPushButton(self)
        self.file_button.setText("Select File")
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(200, 80, 135, 30)

        self.table_text = QLineEdit(self)
        self.db_text = QLineEdit(self)
        self.file_finder_text = QLineEdit(self)

        self.table_label = QLabel(self)
        self.db_label = QLabel(self)
        self.file_finder_label = QLabel(self)

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
        self.progressBar.move(400, 255)
        self.button1.move(280, 255)

        self.button1.clicked.connect(self.enter_button_clicked)
        self.file_button.clicked.connect(self.file_finder)

    # When the enter button is clicked
    def enter_button_clicked(self):
        try:
            if QtCore.Qt.MouseButton.LeftButton:
                # Open CSV file and set the database columns
                file_name = path.basename(self.file_finder_text.text())
                file_name = path.splitext(file_name)[0]
                try:
                    csv_file = open(self.file_finder_text.text())
                    line_amount = len(csv_file.readlines())
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText('Invalid CSV file')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    return

                with open(self.file_finder_text.text(), 'r') as f:
                    type_header = f.readlines()[1].split(",")
                csv_file.seek(0)
                if self.table_text.text() == "":
                    self.table_text.setText(file_name)
                if self.db_text.text() == "":
                    self.db_text.setText(file_name)
                try:
                    conn = connect((self.db_text.text()+'.db'))
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
                for column, type in zip(header, type_header):
                    column = column.replace(" ", "")
                    print(type)
                    if type.isdigit():
                        sql_header_line += column + " int, "
                    else:
                        sql_header_line += column + " nvarchar(255), "
                sql_header_line = sql_header_line[:-2] + ")"
                try:
                    cursor.execute(sql_header_line)
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(
                        'Error creating table, make sure table does not already exist')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    return
                conn.commit()

                # Insert the table contents
                header = [i.replace(" ", "") for i in header]
                contents = csv_file.readlines()[0:]
                cur_line = 0
                for content in contents:
                    cur_line += 1
                    percent_done = int((cur_line/line_amount)*100)
                    self.progressBar.setValue(percent_done)
                    content = content[:-1]
                    content = tuple(content.split(","))
                    sql_insert_line = "INSERT INTO " + \
                        self.table_text.text() + " VALUES (?"
                    for i in range(len(header)-1):
                        sql_insert_line += ", ?"
                    sql_insert_line += ")"
                    cursor.execute(sql_insert_line, content)
                    conn.commit()
                self.progressBar.setValue(100)
                done_msg = QMessageBox()
                done_msg.setWindowTitle('Done')
                done_msg.setText('Conversion Finished')
                done_msg.exec_()
                self.progressBar.setValue(0)
                csv_file.close()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Unknown Error Occurred')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

    # Execute the file finder when the button is pressed
    def file_finder(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.rootPath(), '*.csv')
        self.file_finder_text.setText(file_name)

# Run the app


def runApp():
    connector_app = QApplication([])
    window = MainWindow()
    window.show()
    connector_app.exec()


runApp()
