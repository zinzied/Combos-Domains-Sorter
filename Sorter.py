import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

def sort_combos_by_domain(input_file):
    # Dictionary to hold domain-specific combos
    domain_dict = {}
    seen_combos = set()  # Set to track unique combos
    duplicate_count = 0  # Counter for duplicates

    # Read the input file
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.count('@') == 1 and line.count(':') == 1:
                # Check if the combo is unique
                if line not in seen_combos:
                    seen_combos.add(line)
                    try:
                        username_domain, password = line.split(':', 1)
                        username, domain = username_domain.split('@', 1)
                        
                        # Add the combo to the corresponding domain list
                        if domain not in domain_dict:
                            domain_dict[domain] = []
                        domain_dict[domain].append(line)
                    except ValueError:
                        # Skip lines that don't have the expected format
                        continue
                else:
                    duplicate_count += 1

    # Create output directory if it doesn't exist
    output_dir = 'sorted_combos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write each domain's combos to a separate file
    for domain, combos in domain_dict.items():
        output_file = os.path.join(output_dir, f'{domain}.txt')
        with open(output_file, 'w') as file:
            for combo in sorted(combos):  # Sort the combos before writing
                file.write(combo + '\n')
    
    return duplicate_count, output_dir

class ComboSorterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Combo Domains Sorter | By ZIEDEV')
        self.setGeometry(100, 100, 500, 300)
        
        layout = QVBoxLayout()
        
        # Add banner
        self.banner = QLabel('ZIEDEV ™', self)
        self.banner.setFont(QFont('Arial', 20))
        self.banner.setStyleSheet("color: #ffcc00;")  # Optional: Change color to make it stand out
        self.banner.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.banner)
        
        self.label = QLabel('Select a file to sort combos by domain', self)
        layout.addWidget(self.label)
        
        self.btn_open = QPushButton('Open File', self)
        self.btn_open.clicked.connect(self.showFileDialog)
        layout.addWidget(self.btn_open)
        
        self.btn_sort = QPushButton('Remove Duplicates and Sort', self)
        self.btn_sort.clicked.connect(self.sortFile)
        self.btn_sort.setEnabled(False)  # Disable until a file is selected
        layout.addWidget(self.btn_sort)
        
        self.btn_open_folder = QPushButton('Open Sorted Folder', self)
        self.btn_open_folder.clicked.connect(self.openSortedFolder)
        self.btn_open_folder.setEnabled(False)  # Disable until sorting is done
        layout.addWidget(self.btn_open_folder)
        
        self.setLayout(layout)
        self.input_file = None
        self.output_dir = None
    
    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Combo File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.input_file = fileName
            self.label.setText(f'Selected file: {fileName}')
            self.btn_sort.setEnabled(True)  # Enable the sort button
    
    def sortFile(self):
        if self.input_file:
            self.label.setText(f'Sorting combos in {self.input_file}...')
            duplicate_count, self.output_dir = sort_combos_by_domain(self.input_file)
            self.label.setText(f'Combos sorted and saved in "sorted_combos" directory. Duplicates removed: {duplicate_count}')
            self.btn_open_folder.setEnabled(True)  # Enable the open folder button
    
    def openSortedFolder(self):
        if self.output_dir:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_dir))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Apply dark theme
    dark_stylesheet = """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #3c3f41;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #4c4f51;
    }
    QLabel {
        color: #ffffff;
    }
    """
    app.setStyleSheet(dark_stylesheet)
    
    ex = ComboSorterApp()
    ex.show()
    sys.exit(app.exec_())