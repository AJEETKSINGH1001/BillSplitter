# Bill Splitter Application

A simple Python-based application to help users split the expenses of a trip among multiple participants. The application allows users to add participants, record expenses, and calculate who owes what. It can also generate reports in PDF and Excel formats, save data to a JSON file, and even take screenshots of the UI.

## Features

- **Add Participants**: Easily add participants to the trip.
- **Record Expenses**: Track expenses with details like payer, beneficiaries, and description.
- **Expense Summary**: View detailed expense reports and balances.
- **Settlements**: Optimized settlements between participants to minimize transactions.
- **Save Data**: Save all trip data to a `bill_splitter_data.json` file.
- **Generate Reports**: Generate PDF and Excel reports for the trip expenses.
- **Screenshot**: Take screenshots of the UI for sharing or documentation purposes.

## Requirements

To run this project, you need to have the following Python libraries installed:

- `tkinter`: For the GUI components (pre-installed with Python).
- `openpyxl`: For Excel file generation.
- `reportlab`: For PDF generation.
- `Pillow`: For screenshot functionality.
- `json`: For saving data to a file.

You can install the required libraries by running:

```bash
pip install openpyxl reportlab Pillow

Installation
Clone this repository:

bash
git clone https://github.com/yourusername/bill-splitter.git
Navigate to the project directory:

bash
cd bill-splitter
Install the dependencies:

bash
pip install -r requirements.txt
Usage
Run the application:

bash
python main.py
The user interface will open, and you can start by adding participants and recording expenses.

Steps to Use the Application:
Add Participants: Enter participant names in the provided entry field and click "Add Participant."
Add Expenses: For each expense, provide the amount, payer, beneficiaries, and description. Click "Add Expense" to save it.
View Balances: Click "Show Balances" to see how much each participant owes or is owed.
View Settlements: Click "Show Settlements" to see the optimized list of who should pay whom and how much.
Save Data: Save all entered data into a JSON file by clicking "Save Data."
Generate Report: Generate a PDF or Excel report of all expenses and balances.
Take Screenshot: Take a screenshot of the UI and save it as an image file.
Packaging the Application into an Executable (.exe)
To package this application into a standalone .exe file that can run on Windows without needing Python installed, follow these steps:

1. Install PyInstaller
To install PyInstaller, run:

bash
pip install pyinstaller
2. Create the Executable
In the project directory, run the following command to create a single .exe file:

bash
pyinstaller --onefile --windowed bill_splitter.py
--onefile creates a single .exe file.
--windowed prevents a terminal window from appearing when the app is opened.
3. Locate the Executable
The .exe file will be located in the dist directory. You can find the generated executable at dist/bill_splitter.exe.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Feel free to fork this repository, open an issue, or submit a pull request. If you have ideas for improvements, feel free to contribute!

Acknowledgments
Tkinter for the GUI framework.
ReportLab for generating PDF reports.
OpenPyXL for creating Excel files.
Pillow for screenshot functionality.
vbnet


### How to Use:
- Copy the above text and paste it into a file named `README.md` in the root directory of your project.
- This markdown file should now render properly on GitHub with sections, bullet points, and code block
