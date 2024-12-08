from PySide6.QtWidgets import *
from PySide6.QtGui import *
from fileorganizer import FileOrganizer
from PySide6.QtCore import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.fileorganizer = FileOrganizer()
        self.setFixedSize(600,500)
        self.components()        
        self.events()
    
    def components(self):
        self.list = QListWidget(self)
        self.list.setGeometry(150,50, 400, 350)
        
        self.directory = QLabel(self)
        self.directory.setFixedWidth(500)
        self.directory.setFont(QFont('Arial', 8, QFont.Medium))
        self.directory.setText(self.fileorganizer.current_dir())
        
        self.returnButton = QPushButton('back', self)
        self.returnButton.setGeometry(25, 25, 90, 30)
        
        self.createButton = QPushButton('create', self)
        self.createButton.setGeometry(25, 80, 90, 30)

        self.nameinput = QLineEdit(self);
        self.nameinput.setGeometry(10, 240, 120, 30)
        self.nameinput.hide()
        self.nameinput.setPlaceholderText('new file')
        
        self.renameinput = QLineEdit(self);
        self.renameinput.setGeometry(10, 240, 120, 30)
        self.renameinput.hide()
        self.renameinput.setPlaceholderText('rename')
        
        self.renameButton = QPushButton('rename', self)
        self.renameButton.setGeometry(25, 110, 90, 30)
        self.deleteButton = QPushButton('delete', self)
        self.deleteButton.setGeometry(25, 140, 90, 30)
        self.copyButton = QPushButton('copy', self)
        self.copyButton.setGeometry(25, 170, 90, 30)
        self.moveButton = QPushButton('move', self)
        self.moveButton.setGeometry(25, 200, 90, 30)
        
        self.movelabel = QLabel('sample file' ,self)
        self.movelabel.setGeometry(25, 320, 90, 30)
        self.movelabel.setAlignment(Qt.AlignHCenter)
        self.movelabel.setVisible(False)
        self.moveconfirmButton = QPushButton('confirm', self)
        self.moveconfirmButton.setGeometry(25, 340, 90, 30)
        self.moveconfirmButton.setVisible(False)
        
        self.organizeButton = QPushButton('organize' ,self)
        self.organizeButton.setGeometry(25, 380, 90, 30)
        
    def events(self):
        self.loadFiles()
        self.createButton.clicked.connect(lambda: self.open_inputs(1))
        self.renameButton.clicked.connect(lambda: self.open_inputs(2))
        self.deleteButton.clicked.connect(self.delete_file)
        self.returnButton.clicked.connect(self.back)
        self.list.doubleClicked.connect(self.openFolder)
        self.copyButton.clicked.connect(self.copy_file)

        self.nameinput.returnPressed.connect(self.create_file)
        self.renameinput.returnPressed.connect(self.rename_file)

        self.moveButton.clicked.connect(self.open_moveconfirm_button)
        self.moveconfirmButton.clicked.connect(self.move_file)\
            
        self.organizeButton.clicked.connect(self.organize_files)
        
    def organize_files(self):
        self.fileorganizer.organize()
        self.loadFiles()
    
    def open_moveconfirm_button(self):
        if self.list.selectionModel().hasSelection():
            self.moveButton.setCheckable(True)
            self.movelabel.setText(self.list.currentItem().text())
            self.movelabel.setAccessibleDescription(self.fileorganizer.get_abspath(self.list.currentItem().text()))
        else:
            self.moveButton.setCheckable(False)
            self.movelabel.clear()
        
        if self.moveButton.isChecked() and self.list.selectionModel().hasSelection():
            self.movelabel.setVisible(True)
            self.moveconfirmButton.setVisible(True)
        else:
            self.movelabel.setVisible(False)
            self.moveconfirmButton.setVisible(False)
    
    def move_file(self):
        if not self.movelabel.text() in self.fileorganizer.list():
            file = self.movelabel.accessibleDescription()
            cur_dir = self.fileorganizer.current_dir()
            self.fileorganizer.move(file, cur_dir)
            self.loadFiles()
            self.moveButton.setCheckable(False)
            self.movelabel.clear()
            self.movelabel.setVisible(False)
            self.moveconfirmButton.setVisible(False)
        else:
            print('cant move here')

    def loadFiles(self):
        self.directory.setText(self.fileorganizer.current_dir())
        list = self.fileorganizer.list()
        if self.list.count() != 0:
            self.list.clear()

        for file in list:
            self.list.addItem(Item(file))
    
    def openFolder(self):
        item = self.list.currentItem().text()
        if self.fileorganizer.checkFile(item):
            print('is file')
        else:
            self.fileorganizer.change_dir(item)
        self.loadFiles()

    def back(self):
        self.fileorganizer.return_()
        self.loadFiles()
        
    def create_file(self):
        item = self.nameinput.text().strip()

        if item:
            self.fileorganizer.create_item(item)
            self.loadFiles()
            self.nameinput.clear()
            self.nameinput.hide()
    
    def rename_file(self):
        if self.list.selectionModel().hasSelection():
            filename= self.list.currentItem().text()
            name = self.renameinput.text().strip()
            
            if name:
                self.fileorganizer.rename(filename, name)
                self.loadFiles()
                self.renameinput.clear()
                self.renameinput.hide()
        
    def delete_file(self):
        if self.list.selectionModel().hasSelection():
            item = self.list.currentItem().text()
            self.fileorganizer.delete_item(item)
            self.loadFiles()

    def copy_file(self):
        if self.list.selectionModel().hasSelection():
            item = self.list.currentItem().text().strip()
            
            if item:
                self.fileorganizer.copy(item)                
                self.loadFiles()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.nameinput.clear()
            self.renameinput.clear()
            self.nameinput.hide()
            self.renameinput.hide()
            self.list.clearSelection()
            
        return super().keyPressEvent(event)
    
    def open_inputs(self, input_number):
        if input_number == 1:
            self.nameinput.show()
            self.renameinput.clear()
            self.renameinput.hide()
            
        elif input_number == 2:
            self.renameinput.show()
            self.nameinput.clear()
            self.nameinput.hide()
    
    
class Item(QListWidgetItem):
    def __init__(self, label):
        super().__init__(label)
        self.setFont(QFont("Arial", 16, QFont.Medium))