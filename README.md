### Combo Sorter Application

The Combo Sorter application is a user-friendly, GUI-based tool designed to help users manage and organize email-password combinations (combos) by their domain names. It is built using PyQt5, a set of Python bindings for the Qt application framework.


 ![photo_5830135848115487868_w (1)](https://github.com/user-attachments/assets/e7c9e56c-a689-4e0b-9de7-8e73c31a73a1)

### Key Features

1. **File Selection**: Users can easily select a text file containing email-password combos through a file dialog.
2. **Sorting and Deduplication**: The application sorts the combos by their domain names and removes any duplicate entries.
3. **Output Directory**: Sorted combos are saved into separate files within a specified output directory (`sorted_combos`).
4. **Open Folder**: A convenient button allows users to open the folder containing the sorted files directly from the application.
5. **Dark Theme**: The application features a dark theme for a modern and visually appealing interface.

### How to Use the Application

1. **Launch the Application**:
   - Install requirements (e.g., `pip install -r requirements.txt`)
   - Run the Python script (e.g., `combo_sorter.py`) to launch the application.

3. **Select a File**:
   - Click the "Open File" button to open a file dialog.
   - Navigate to the location of your text file containing the email-password combos and select it.
   - The selected file's path will be displayed in the application.

4. **Sort and Remove Duplicates**:
   - Once a file is selected, the "Remove Duplicates and Sort" button will be enabled.
   - Click this button to start the sorting and deduplication process.
   - The application will read the file, sort the combos by domain, remove duplicates, and save the sorted combos into separate files within the `sorted_combos` directory.
   - A message will be displayed indicating the number of duplicates removed and confirming that the sorted combos have been saved.

5. **Open Sorted Folder**:
   - After the sorting process is complete, the "Open Sorted Folder" button will be enabled.
   - Click this button to open the `sorted_combos` directory in your default file explorer, where you can view the sorted combo files.

### Example Workflow

1. **Start the Application**:
   - Double-click the Python script or run it from the command line using `python combo_sorter.py`.

2. **Select a Combo File**:
   - Click "Open File".
   - Select `combos.txt` or any other text file containing email-password combos.

3. **Sort and Remove Duplicates**:
   - Click "Remove Duplicates and Sort".
   - Wait for the process to complete. The application will display a message like:
     ```
     Combos sorted and saved in "sorted_combos" directory. Duplicates removed: 10
     ```

4. **Open the Sorted Folder**:
   - Click "Open Sorted Folder".
   - The `sorted_combos` directory will open, showing files named after the domains (e.g., `example.com.txt`, `mail.com.txt`).

### Technical Details

- **Imports**: The application imports necessary modules from PyQt5 and standard Python libraries.
- **sort_combos_by_domain Function**: This function reads the input file, sorts the combos by domain, removes duplicates, and writes the sorted combos to separate files.
- **ComboSorterApp Class**: This class defines the main window of the application, including the UI elements and their functionalities.
- **Main Execution Block**: This block initializes the application, applies the dark theme, and starts the event loop.
### Donations
If you feel like showing your love and/or appreciation for this Sipmle project, then how about shouting me a coffee or Milk :)

[<img src="https://github.com/zinzied/Website-login-checker/assets/10098794/24f9935f-3637-4607-8980-06124c2d0225">](https://www.buymeacoffee.com/Zied)


