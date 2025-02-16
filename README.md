# CSVCompareProgram
CSV Comparison Tool
Description

This Python-based GUI tool allows you to compare CSV files to identify missing devices between two lists (e.g., Antivirus and Monitoring systems). It displays which devices are missing and provides a clear output of the differences.

Features

Compare multiple CSV files simultaneously (for Antivirus and Monitoring).
Customizable column names to identify device names.
Display of missing devices in a clear text output.
Reset function for each file group (Antivirus/Monitoring).
Warning when running the comparison again without resetting.
Requirements

Python 3.x
Required libraries: pandas, tkinter
Installing Dependencies

If pandas is not installed, it can be installed with the following command:

bash
Kopieren
Bearbeiten
pip install pandas
Usage

Start the Program:

bash
Kopieren
Bearbeiten
python csv_comparison_tool.py
Select Files:

Click on "Add Antivirus CSV(s)" or "Add Monitoring CSV(s)" to load the corresponding CSV files.

Multiple files can be selected at once.

Enter Column Names:

Enter the name of the column containing the device names in the fields below the file selection buttons (default is "Name").

Run Comparison:

Click on "Run Comparison" to analyze the differences between the Antivirus and Monitoring files.

The result will be displayed in the text field.

Reset:

The "Reset" button allows you to remove the selected files and prepare for a new comparison.

Example Output

Device Name: PC1 | Missing: Monitoring
Device Name: SERVER2 | Missing: Monitoring
Device Name: Server03 | Missing: Antivirus
Notes

Duplicate Device Names: If there is no unique identification (e.g., by location) in the CSV files, duplicate device names cannot be uniquely mapped.
Empty Rows: Empty or invalid entries in the CSV files are automatically filtered out.
Creating an Executable

The script can be converted into a standalone executable using pyinstaller:

bash
Kopieren
Bearbeiten
pip install pyinstaller
pyinstaller --onefile csv_comparison_tool.py
The executable file will be located in the dist directory.

Troubleshooting

Error with Column Names: Check if the provided column names are present in all CSV files.
Missing Results: Ensure that the files are read correctly and do not contain empty rows.
License

This project is licensed under the GPL 3.0 License for non-commercial use. For commercial use, please contact the author for a separate license.
