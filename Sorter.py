import os
import sys
import json
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMenu, QProgressBar, QLineEdit
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

def sanitize_filename(domain):
    """Sanitize domain name for use as filename"""
    # Replace invalid filename characters with underscore
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', domain)
    # Limit filename length to avoid path length issues
    return sanitized[:250] if len(sanitized) > 250 else sanitized

def sort_combos_by_domain(input_file, progress_callback=None):
    try:
        # Try to count lines with utf-8 encoding
        total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8', errors='ignore'))
    except Exception:
        # Fallback to counting lines with latin-1 encoding if utf-8 fails
        total_lines = sum(1 for _ in open(input_file, 'r', encoding='latin-1'))

    current_line = 0
    domain_dict = {}
    seen_combos = set()
    duplicate_count = 0

    # Try different encodings
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    file_content = None

    for encoding in encodings_to_try:
        try:
            with open(input_file, 'r', encoding=encoding, errors='ignore') as file:
                for line in file:
                    line = line.strip()
                    if line.count('@') == 1 and line.count(':') == 1:
                        if line not in seen_combos:
                            seen_combos.add(line)
                            try:
                                username_domain, password = line.split(':', 1)
                                username, domain = username_domain.split('@', 1)
                                if domain not in domain_dict:
                                    domain_dict[domain] = []
                                domain_dict[domain].append(line)
                            except ValueError:
                                continue
                        else:
                            duplicate_count += 1
                    current_line += 1
                    if progress_callback:
                        progress_callback(int((current_line/total_lines) * 100))
            break  # If successful, break the encoding loop
        except UnicodeDecodeError:
            continue  # Try next encoding
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")

    # Create output directory if it doesn't exist
    output_dir = 'sorted_combos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write each domain's combos to a separate file
    for domain, combos in domain_dict.items():
        safe_domain = sanitize_filename(domain)
        output_file = os.path.join(output_dir, f'{safe_domain}.txt')
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                for combo in sorted(combos):
                    file.write(combo + '\n')
        except OSError as e:
            raise Exception(f"Error writing file for domain {domain}: {str(e)}")
    
    return duplicate_count, output_dir

class ComboSorterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadSettings()
    
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

        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        # Add report button to UI
        self.btn_report = QPushButton('Generate Report', self)
        self.btn_report.clicked.connect(self.generate_report)
        self.btn_report.setEnabled(False)  # Disable initially
        layout.addWidget(self.btn_report)

        # Add search box to UI
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search domains...")
        self.search_box.textChanged.connect(self.filterDomains)
        layout.addWidget(self.search_box)

        # Add to UI class
        self.stats_label = QLabel('', self)
        self.stats_label.setStyleSheet("color: #00ff00;")
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        self.input_file = None
        self.output_dir = None

        self.createContextMenu()
    
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
            try:
                self.label.setText(f'Sorting combos in {self.input_file}...')
                self.domain_dict = {}
                self.duplicate_count, self.output_dir = sort_combos_by_domain(
                    self.input_file, 
                    progress_callback=self.progress.setValue
                )
                self.total_combos = sum(len(combos) for combos in self.domain_dict.values())
                self.domains_count = len(self.domain_dict)
                self.stats_label.setText(
                    f'Total domains: {self.domains_count}\n'
                    f'Total valid combos: {self.total_combos}\n'
                    f'Duplicates removed: {self.duplicate_count}'
                )
                self.label.setText(
                    f'Combos sorted and saved in "sorted_combos" directory. '
                    f'Duplicates removed: {self.duplicate_count}'
                )
                self.btn_open_folder.setEnabled(True)
                self.btn_report.setEnabled(True)  # Enable report button after successful sort
            except Exception as e:
                self.label.setText(f'Error: {str(e)}')
                self.label.setStyleSheet("color: red;")
    
    def openSortedFolder(self):
        if self.output_dir:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_dir))

    def saveSettings(self):
        settings = {
            'last_directory': os.path.dirname(self.input_file) if self.input_file else '',
            'window_geometry': self.geometry().getRect(),
            'dark_mode': True  # Add theme toggle option
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def loadSettings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                # Apply settings
                if settings['last_directory']:
                    self.last_directory = settings['last_directory']
        except FileNotFoundError:
            pass

    # Add context menu for copying domain stats
    def createContextMenu(self):
        menu = QMenu(self)
        copyAction = menu.addAction("Copy Statistics")
        copyAction.triggered.connect(self.copyStats)

    def copyStats(self):
        clipboard = QApplication.clipboard()
        stats_text = self.stats_label.text()
        clipboard.setText(stats_text)

    def generate_report(self):
        if not self.output_dir or not hasattr(self, 'domain_dict'):
            self.label.setText('Error: Please sort a file first before generating a report')
            self.label.setStyleSheet("color: red;")
            return

        try:
            report_path = os.path.join(self.output_dir, '_summary_report.txt')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Combo Sorting Report\n")
                f.write(f"==================\n")
                f.write(f"Input file: {self.input_file}\n")
                f.write(f"Total domains processed: {self.domains_count}\n")
                f.write(f"Total valid combos: {self.total_combos}\n")
                f.write(f"Duplicates removed: {self.duplicate_count}\n\n")
                f.write("Domain Statistics:\n")
                f.write("=================\n")
                # Sort domains by combo count
                sorted_domains = sorted(self.domain_dict.items(), 
                                     key=lambda x: len(x[1]), 
                                     reverse=True)
                for domain, combos in sorted_domains:
                    f.write(f"{domain}: {len(combos)} combos\n")
            
            self.label.setText(f'Report generated: {report_path}')
            self.label.setStyleSheet("color: #00ff00;")
        except Exception as e:
            self.label.setText(f'Error generating report: {str(e)}')
            self.label.setStyleSheet("color: red;")

    def filterDomains(self):
        search_term = self.search_box.text().lower()
        output_dir = 'sorted_combos'
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                if search_term in file.lower():
                    # Highlight or show matching domains
                    pass

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
