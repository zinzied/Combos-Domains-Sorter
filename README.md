This Simple App. is a PyQt5-based GUI application designed to sort email-password combinations (combos) by their domain and remove duplicates. The application allows the user to select a text file containing the combos, processes the file to remove duplicates, sorts the combos by domain, and saves the sorted combos into separate files based on their domains. Additionally, the GUI has a dark theme applied to it.

### Key Components:

1. **Function `sort_combos_by_domain(input_file)`**:
   - **Purpose**: Reads the input file, removes duplicate combos, sorts them by domain, and writes the sorted combos to separate files.
   - **Parameters**: `input_file` - the path to the input file containing the combos.
   - **Process**:
     - Initializes a dictionary `domain_dict` to store domain-specific combos and a set `seen_combos` to track unique combos.
     - Reads the input file line by line, checks if the line is a valid combo (contains exactly one '@' and one ':'), and adds it to the set if it's unique.
     - Splits the combo into username and domain, and stores it in the dictionary under the corresponding domain.
     - Counts the number of duplicates encountered.
     - Creates an output directory `sorted_combos` if it doesn't exist.
     - Writes each domain's combos to a separate file, sorted alphabetically.
   - **Returns**: The number of duplicates removed.

2. **Class `ComboSorterApp(QWidget)`**:
   - **Purpose**: Defines the main GUI application.
   - **Methods**:
     - `__init__(self)`: Initializes the GUI components.
     - `initUI(self)`: Sets up the GUI layout, including labels and buttons.
     - `showFileDialog(self)`: Opens a file dialog for the user to select a combo file. Enables the sort button once a file is selected.
     - `sortFile(self)`: Calls `sort_combos_by_domain` to process the selected file and updates the label to show the number of duplicates removed.

3. **Main Execution Block**:
   - Creates a `QApplication` instance.
   - Applies a dark theme to the application using a stylesheet.
   - Creates an instance of `ComboSorterApp` and displays the GUI.
   - Starts the application's event loop with `sys.exit(app.exec_())`.

### Dark Theme Stylesheet:
- **QWidget**: Sets the background color to dark gray (`#2b2b2b`) and text color to white (`#ffffff`).
- **QPushButton**: Sets the background color to a slightly lighter gray (`#3c3f41`), text color to white, and border color to a medium gray (`#555555`). Changes the background color on hover to an even lighter gray (`#4c4f51`).
- **QLabel**: Sets the text color to white.

### User Interaction:
1. The user launches the application.
2. The user clicks the "Open File" button to select a combo file.
3. The user clicks the "Remove Duplicates and Sort" button to process the file.
4. The application processes the file, removes duplicates, sorts the combos by domain, and saves the results in the `sorted_combos` directory.
5. The label updates to show the number of duplicates removed.

This code provides a simple yet functional GUI for sorting and deduplicating email-password combos, with a modern dark theme for better visual appeal.
