
# LeetForces CPH Extension

This Extension is used to fecth leetcode test cases by just entering the url of the problem link then the user can run his/her solution (python/cpp) against those fetched test cases by writing his solution in the provided solution template and can compare the expected and actual outputs.



## Features

- Easily scraps the leetcode webpage to fetch test cases
- Option to Manage the test cases such as view,edit,remove and add test cases 
- Test cases are saved in the respective test_cases named folder in the directory
- Users can write solution in python and cpp easily.
- Compares the user's solution output and the fetched test cases output
- Proper erros and clean dailog boxes shown for any information


## Installation

Follow these steps to set up the project on your local machine: 

1. Prerequisites
Before you begin, ensure you have the following installed on your machine:

- Python (3.8 or higher)
- Node.js (14.x or higher) and npm (Node Package Manager)
- g++ or any C++ compiler for running C++ files
- Google Chrome (for Selenium automation)
- Chromedriver (compatible with your Chrome version)

2. Install Python Dependencies
Install the required Python modules. Run the following command:

```bash
pip install ast selenium
```
3. Install Node.js Packages
Navigate to the project directory and install the required npm packages:

```bash
npm install
```

4. Download Chromedriver
- Identify your Google Chrome version:
- Open Chrome.
- Navigate to chrome://settings/help to find the version.
- Download the matching Chromedriver version:
- Go to Chromedriver Downloads.
- Download the driver matching your Chrome version and operating system.
- Add Chromedriver to your system's PATH:
- Move the downloaded Chromedriver file to a directory included in your system PATH.
- Alternatively, keep it in your project directory and update its path in your scripts.

5. Set Up the Project
- Clone the repository:
```bash
git clone https://github.com/Anuj-m02/Leetforces-CPH-.git
```
- Navigate to the project directory:
```bash
cd Leetforces-CPH-
```
6. Run the Extension
- Launch Visual Studio Code.
- Open the project directory.
- Press F5 or run the project as a VScode extension to start using the commands by pressing Ctrl+Shift+P which opens the command pallete.
## Ensure
- Ensure selenium and all other modules are installed properly .
- Ensure you have added the correct chromedriver path here.
![App Screenshot](https://github.com/user-attachments/assets/ffa22cb1-5c86-4739-80fc-24fbf40d4a09)

- In the extension.ts file just ensure everything is imported rightly and user will write his code in the provided Solution Class Template same as of Leetcode ...
![App ScreenShot](https://github.com/user-attachments/assets/83e39b92-2016-4e41-af94-d30760147ce3)

## Usage 
- Press F5 to launch the extension in a new Extension Development Host window.
- Use the following commands available in the Command Palette (Ctrl + Shift + P):
1. Fetch LeetCode Test Cases
- Open the desired LeetCode problem in your VS Code workspace.
- Run the `Fetch LeetCode Test Cases` command from the Command Palette.
- Enter the LeetCode problem URL in the input prompt.
- The extension will fetch the problem's test cases and save them in a testCase folder in your workspace directory.
- Input Files: Saved as input_X.txt, where X is the test case number.
- Output Files: Saved as output_X.txt, containing the expected outputs.
2. Manage LeetCode Test Cases
- Use the `Manage LeetCode Test Cases` command to organize or modify the test cases stored in the testCase folder.
- You can add, delete, or update test cases as needed directly within this folder to refine your testing process.
3. Write Solution
- Run the `Write Solution` command to generate a boilerplate file for solving a LeetCode problem.
- This will create a solution template file in your workspace, preconfigured with the necessary setup to begin coding.
4. LeetForces Run Solution
- After fetching the test cases and writing your solution:
Run the `LeetForces Run Solution` command from the Command Palette.
- The extension will execute your code with the fetched test cases.
- It will compare your solution’s output with the expected output and display the results in the terminal.
  
## Demo Video

![Leetforces demo video](https://github.com/user-attachments/assets/a1782dda-54ec-4ba3-b908-8454f13e137f)

- File Selection Menu wasnt recorded (gif length :(  issue... ) , though a dialog box will open for the user to select the solution file...  
## Commands

- `Write Solution` : Generates a boilerplate file for solving a LeetCode problem in your workspace, helping you get started with your solution.

- `Fetch LeetCode Test Cases` : Prompts the user for a LeetCode problem URL, fetches the test cases for that problem, and saves them in the testCase folder.

- Input files are stored as `input_X.txt`, and expected output files are stored as `output_X.txt`.
- `LeetForces Run Solution` : Executes your solution against the fetched test cases and displays the results, showing whether your solution matches the expected output.

- `Manage LeetCode Test Cases` : Provides tools to manage the test cases stored in the testCase folder. You can add, edit, or delete test cases as needed to improve your testing process.