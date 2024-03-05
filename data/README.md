# MyMup Data Tool: Quarterly Report Generator

## Overview
MyMup Data Tool is designed to automate the process of generating quarterly reports from structured data files. This tool takes in CSV files, performs data cleaning, validation, and analysis, and outputs a comprehensive report. It features a user-friendly GUI for easy operation.

## Prerequisites
- Python 3.6 or higher
- pandas
- tkinter

## Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/edheyev/MyMupDataTool.git
cd MyMupDataTool
```

2. Set up a virtual environment (optional but recommended):
```bash
python -m venv myenv
source myenv/Scripts/activate  # On Windows
source myenv/bin/activate  # On Unix or MacOS
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if you set it up):
```bash
source myenv/Scripts/activate  # On Windows
source myenv/bin/activate  # On Unix or MacOS
```

2. Run the script using Python:
```bash
python data_flow_qr.py
```

3. Use the GUI to select the folder containing all required data files. Ensure the files are named correctly as per the documentation and match the specified column structure.

4. Enter the start and end dates for the reporting period in the format `YYYY-MM-DD`.

5. Click on "Start Processing" to begin the report generation process.

## File Structure Requirements
The data files should be named according to the following convention:
- contacts_or_indirects_within_reporting_period.csv
- mib_contacts_or_indirects_within_reporting_period.csv
- file_closures_and_goals_within_reporting_period.csv
- ... (additional file naming conventions as per your requirements)

Ensure the files adhere to the expected column structures as outlined in the documentation.

## Troubleshooting
If you encounter any issues, ensure that:
- You have the correct version of Python installed.
- All required dependencies are installed in the virtual environment.
- The CSV files are named correctly and placed in the designated folder.



---

# Building Executable with PyInstaller (notes for me)

This document explains how to create a standalone executable from a Python script using PyInstaller within a virtual environment on Windows.

## Prerequisites

- Python installed on your system
- Virtual environment created and activated
- PyInstaller installed within the virtual environment

## Steps

1. **Activate Virtual Environment**

   Navigate to your project directory and activate the virtual environment:

   ```bash
   source ./myenv/Scripts/activate
   ```

   You should see `(myenv)` before the command prompt, indicating that the virtual environment is active.

2. **Install PyInstaller (if not already installed)**

   If PyInstaller is not installed within the virtual environment, install it using pip:

   ```bash
   pip install pyinstaller
   ```

3. **Run PyInstaller**

   To run PyInstaller and build your executable, use the following command:

   ```bash
   ./myenv/Scripts/python.exe -m PyInstaller data_flow_mr.spec
   ```

   Replace `your_script.spec` with the name of your PyInstaller spec file.

   This command uses the Python executable from the virtual environment to run PyInstaller as a module.

4. **Troubleshooting**

   If you encounter the error "No module named PyInstaller", ensure that you are in the virtual environment and that PyInstaller is installed by running:

   ```bash
   pip show pyinstaller
   ```

   If PyInstaller is not listed, install it using the pip install command above.

## Notes

- Always ensure that the virtual environment is activated before running PyInstaller.
- The spec file should be located in the same directory where you're running the command, or provide the relative path to it.
- After building the executable, you can find it in the `dist` directory created by PyInstaller.

Remember to deactivate your virtual environment when you're done:

```bash
deactivate
```

## Conclusion

By following these steps, you can consistently build your Python application into a standalone executable using PyInstaller in a Windows environment.
