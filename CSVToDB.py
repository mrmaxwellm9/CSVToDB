import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import *
######################################


class MainWindow(QMainWindow):
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

    def enter_button_clicked(self):
        if QtCore.Qt.MouseButton.LeftButton:
            conn = sqlite3.connect((self.db_text.text()+'.db'))
            cursor = conn.cursor()

            csv_file = open(self.file_finder_text.text())
            header = csv_file.readline().split(",")
            header[-1] = header[-1][:-1]
            sql_header_line = 'CREATE TABLE ' + self.table_text.text() + '('
            for column in header:
                column = column.replace(" ", "")
                if isinstance(column, int):
                    sql_header_line += column + " int, "
                else:
                    sql_header_line += column + " nvarchar(255), "
            sql_header_line = sql_header_line[:-2] + ")"

            cursor.execute(sql_header_line)
            conn.commit()

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
                print(sql_insert_line)
                print(content)
                cursor.execute(sql_insert_line, content)
                conn.commit()
            csv_file.close()

    def file_finder(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Single File', QtCore.QDir.rootPath(), '*.csv')
        self.file_finder_text.setText(file_name)


connector_app = QApplication([])
window = MainWindow()
window.show()
connector_app.exec()

# # Insert DataFrame to Table
# for row in df.itertuples():
#     cursor.execute('''
#                 INSERT INTO products (product_id, product_name, price)
#                 VALUES (?,?,?)
#                 ''',
#                    row.product_id,
#                    row.product_name,
#                    row.price
#                    )
