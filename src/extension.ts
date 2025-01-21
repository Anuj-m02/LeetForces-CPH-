import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, spawnSync } from 'child_process';

// Create a reusable function to log messages
function logMessage(outputChannel: vscode.OutputChannel, message: string) {
    outputChannel.appendLine(message);
    console.log(message);
}

// Fetch settings dynamically
function getConfiguration(key: string): string {
    const config = vscode.workspace.getConfiguration('leetforces');
    return config.get<string>(key) || '';
}

export function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel('LeetForces');
    logMessage(outputChannel, 'LeetForces Extension Activated');

    // Command to fetch test cases
    const fetchTestCasesCommand = vscode.commands.registerCommand('leetcode.fetchTestCases', async () => {
        const url = await vscode.window.showInputBox({ prompt: 'Enter LeetCode problem URL' });
        if (!url) {
            vscode.window.showErrorMessage('URL is required!');
            return;
        }

        const scriptPath = path.join(context.extensionPath, 'src', 'fetch_test_cases.py');
        const pythonCommand = 'python';
        const args = [scriptPath, 'fetch', url];

        logMessage(outputChannel, `Executing command: ${pythonCommand} ${args.join(' ')}`);
        const fetchProcess = spawn(pythonCommand, args, { cwd: context.extensionPath });

        fetchProcess.stdout.on('data', (data) => logMessage(outputChannel, data.toString()));
        fetchProcess.stderr.on('data', (data) => logMessage(outputChannel, `Error: ${data.toString()}`));

        fetchProcess.on('close', (code) => {
            if (code === 0) {
                vscode.window.showInformationMessage('Test cases fetched successfully!');
                logMessage(outputChannel, 'Fetch Test Cases completed successfully.');
            } else {
                vscode.window.showErrorMessage(`Fetch Test Cases failed with code ${code}.`);
                logMessage(outputChannel, `Fetch Test Cases exited with code ${code}.`);
            }
        });
    });

 // Command to manage test cases (view, edit, add, remove)
const manageTestCasesCommand = vscode.commands.registerCommand('leetcode.manageTestCases', async () => {
    const action = await vscode.window.showQuickPick(['view', 'edit', 'add', 'remove'], {
        placeHolder: 'Select action for test cases'
    });

    if (!action) {
        vscode.window.showErrorMessage('No action selected!');
        return;
    }

    const scriptPath = path.join(context.extensionPath, 'src', 'fetch_test_cases.py');
    const pythonCommand = 'python';
    let args: string[] = [];

    if (action === 'view') {
        args = [scriptPath, 'manage', 'view'];
    } else if (action === 'edit') {
        const fileName = await vscode.window.showInputBox({ prompt: 'Enter the file name to edit (e.g., input_1.txt)' });
        if (!fileName) {
            vscode.window.showErrorMessage('File name is required to edit!');
            return;
        }

        const newContent = await vscode.window.showInputBox({ prompt: 'Enter the new content for the test case' });
        if (!newContent) {
            vscode.window.showErrorMessage('New content is required!');
            return;
        }

        args = [scriptPath, 'manage', 'edit', fileName, newContent];
    } else if (action === 'add') {
        const inputData = await vscode.window.showInputBox({ prompt: 'Enter input data for the new test case' });
        const outputData = await vscode.window.showInputBox({ prompt: 'Enter output data for the new test case' });

        if (!inputData || !outputData) {
            vscode.window.showErrorMessage('Both input and output data are required to add a new test case!');
            return;
        }
        args = [scriptPath, 'manage', 'add', inputData, outputData];
    } else if (action === 'remove') {
        const index = await vscode.window.showInputBox({ prompt: 'Enter the index of the test case to remove (e.g., 1 for input_1.txt/output_1.txt)' });

        if (!index || isNaN(Number(index))) {
            vscode.window.showErrorMessage('A valid test case index is required to remove a test case!');
            return;
        }

        args = [scriptPath, 'manage', 'remove', index];
    }

    logMessage(outputChannel, `Executing command: ${pythonCommand} ${args.join(' ')}`);
    const manageProcess = spawn(pythonCommand, args, { cwd: context.extensionPath });

    manageProcess.stdout.on('data', (data) => logMessage(outputChannel, data.toString()));
    manageProcess.stderr.on('data', (data) => logMessage(outputChannel, `Error: ${data.toString()}`));

    manageProcess.on('close', (code) => {
        if (code === 0) {
            vscode.window.showInformationMessage(`${action.charAt(0).toUpperCase() + action.slice(1)} test cases completed successfully!`);
            logMessage(outputChannel, `${action.charAt(0).toUpperCase() + action.slice(1)} Test Cases completed successfully.`);
        } else {
            vscode.window.showErrorMessage(`${action.charAt(0).toUpperCase() + action.slice(1)} Test Cases failed with code ${code}.`);
            logMessage(outputChannel, `${action.charAt(0).toUpperCase() + action.slice(1)} Test Cases exited with code ${code}.`);
        }
    });
});

    // write solution command 
    const writeSolutionCommand = vscode.commands.registerCommand("leetcode.writeSolution", async () => {
        try {
            // Prompt for problem name
            const problemName = await vscode.window.showInputBox({ prompt: "Enter problem name or ID" });
            if (!problemName) {
                vscode.window.showErrorMessage("Problem name or ID is required!");
                return;
            }
    
            // Prompt for language
            const language = await vscode.window.showQuickPick(["python", "cpp"], {
                placeHolder: "Select the language for your solution",
            });
            if (!language) {
                vscode.window.showErrorMessage("No language selected!");
                return;
            }
    
            // Paths for test cases and parsing script
            const testCaseDir = path.join(context.extensionPath, "test_cases");
            const parseinputScriptPath = path.join(context.extensionPath, "src", "parse_input.py");
            const parseoutputScriptPath = path.join(context.extensionPath, "src", "parse_output.py");
            const inputFilePath = path.join(testCaseDir, "input_1.txt");
            const outputFilePath = path.join(testCaseDir, "output_1.txt");
    
            // Ensure the test case directory and input/output files exist
            if (!fs.existsSync(testCaseDir)) {
                vscode.window.showErrorMessage("Test case directory does not exist!");
                return;
            }
            if (!fs.existsSync(inputFilePath)) {
                vscode.window.showErrorMessage("Input file does not exist!");
                return;
            }
            if (!fs.existsSync(outputFilePath)) {
                vscode.window.showErrorMessage("Output file does not exist!");
                return;
            }
    
            // Run parse.py for input file
            const pythonCommand = "python";
            const inputChild = spawnSync(pythonCommand, [parseinputScriptPath, inputFilePath], {
                encoding: "utf8",
                cwd: context.extensionPath,
            });
            if (inputChild.error || !inputChild.stdout) {
                vscode.window.showErrorMessage("Failed to parse input keys. Ensure your input file is valid.");
                return;
            }
    
            // Parse input JSON
            let inputKeys: string[] = [];
            let inputTypes: string[] = [];
            try {
                const inputOutput = JSON.parse(inputChild.stdout);
                inputKeys = inputOutput.keys || [];
                inputTypes = inputOutput.types || [];
            } catch (error) {
                vscode.window.showErrorMessage("Failed to parse input keys and types. Check the console for details.");
                return;
            }
    
            // Run parse.py for output file
            const outputChild = spawnSync(pythonCommand, [parseoutputScriptPath, outputFilePath], {
                encoding: "utf8",
                cwd: context.extensionPath,
            });
            if (outputChild.error || !outputChild.stdout) {
                vscode.window.showErrorMessage("Failed to parse output type. Ensure your output file is valid.");
                return;
            }
    
            // Parse output JSON
            let outputType: string = "";
            try {
                const outputOutput = JSON.parse(outputChild.stdout);
                outputType = outputOutput.type || "";
            } catch (error) {
                vscode.window.showErrorMessage("Failed to parse output type. Check the console for details.");
                return;
            }
    
            // Logic to handle C++ types and map them to Python types
            const convertTypeForPython = (cppType: string): string => {
                if (cppType === "vector<vector<int>>") {return "list[list[int]]";}
                if (cppType === "vector<vector<string>>") {return "list[list[str]]";}
                if (cppType === "vector<int>") { return "list[int]"; }
                if (cppType === "vector<string>") { return "list[str]"; }
                if (cppType === "vector<char>") { return "list[str]";}
                if (cppType === "string") { return "str";}
                if (cppType === "vector<bool>") {return "list[bool]";}
                if (cppType === "double") {return  "float";}
                return cppType; // Fallback
            };
    
            const convertTypeForCpp = (cppType: string): string => {
                if (cppType.startsWith("list[")) {
                    return cppType.replace("list[", "vector<").replace("]", ">");
                }
                //add conditoins for listliststr listlistint str int 
                return cppType; // Fallback
            };
    
            // Generate argument lists for Python and C++
            let pythonArgs = "";
            let cppArgs = "";
    
            if (language === "python") {
                pythonArgs = inputKeys
                    .map((key, index) => `${key}: ${convertTypeForPython(inputTypes[index])}`)
                    .join(", ");
            } else if (language === "cpp") {
                cppArgs = inputKeys
                    .map((key, index) => `${inputTypes[index]} ${key}`)
                    .join(", ");
            }
    
            // Convert output type for the selected language
            const pythonReturnType = convertTypeForPython(outputType);
            const cppReturnType = convertTypeForCpp(outputType);
    
            // Define solution templates
            const templates: { [key: string]: string } = {
                python: `
class Solution:
    def solve(self, ${pythonArgs}) -> ${pythonReturnType}:
            # Write your solution logic here
            pass
                `,
                cpp: `#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    // Solve function which will accept the parsed inputs
    ${cppReturnType} solve(${cppArgs}) {
        // Write your solution logic here
        // Example: return some processed value based on input
    }
};

// Overload the << operator for printing vectors
ostream& operator<<(ostream& os, const vector<int>& vec) {
    for (const auto& item : vec) {
        os << item << " ";  // Print each element with space
    }
    return os;
}

ostream& operator<<(ostream& os, const vector<vector<int>>& vec) {
    for (const auto& subVec : vec) {
        os << "[";
        for (const auto& item : subVec) {
            os << item << " ";
        }
        os << "] ";
    }
    return os;
}

ostream& operator<<(ostream& os, const vector<string>& vec) {
    for (const auto& item : vec) {
        os << "\"" << item << "\" ";  // Print each string surrounded by quotes
    }
    return os;
}
ostream& operator<<(ostream& os, const vector<char>& vec) {
    for (const auto& item : vec) {
        os << item << " ";  // Print each character with space
    }
    return os;
}

int main() {
    Solution solution;
        int x;             // Declare integer variable for vector<int> and vector<vector<int>>
        string line;       // Declare string variable for vector<vector<int>>
        string word;       // Declare string variable for vector<string>
        char ch;           // Declare char variable for vector<char>            
    // Input parsing based on argument types
    ${cppArgs.split(", ").map((arg, index) => {
        const [type, name] = arg.split(" ");
        
        // Handling different types based on their input format
        if (type === "vector<int>") {
            return `${type} ${name};\n    while (cin >> x) { ${name}.push_back(x); if (cin.peek() == '\\n') break; }`;  // vector input style
        } else if (type === "vector<vector<int>>") {
            return `${type} ${name};\n    while (getline(cin, line)) {\n        if (line.empty()) break;\n        istringstream iss(line);\n        vector<int> tempVec;\n        int x;\n        while (iss >> x) tempVec.push_back(x);\n        ${name}.push_back(tempVec);\n    }`;  // vector<vector<int>> input style
        } else if (type === "vector<string>") {
            return `${type} ${name};\n    while (cin >> word) { ${name}.push_back(word); if (cin.peek() == '\\n') break; }`;  // vector<string> input style
        } else if (type === "vector<char>") {
            return `${type} ${name};\n    while (cin >> ch) { ${name}.push_back(ch); if (cin.peek() == '\\n') break; }`;  // vector<char> input style
        } else if (type === "int") {
            return `${type} ${name};\n    cin >> ${name};`;  // Single integer input
        } else if (type === "string") {
            return `${type} ${name};\n    cin >> ${name};`;  // String input
        } else if (type === "bool") {
            return `${type} ${name};\n    cin >> ${name};`; // bool input 
        }
        return `${type} ${name};`; // Default handling for other types
    }).join("\n    ")}

    // Call solve function with the initialized input arguments
    ${cppReturnType} result = solution.solve(${inputKeys.join(", ")});
    
    // Output handling
    cout << result << endl;  // For types like int, string, vector<int>, etc.

    return 0;
}
`,
            };
    
            // Create solution file based on the selected language
            const solutionTemplate = templates[language].trim();
            const solutionFileName = `${problemName}.${language === "python" ? "py" : "cpp"}`;
            const solutionFilePath = path.join(vscode.workspace.rootPath || context.extensionPath, solutionFileName);
    
            // Write the solution file and open it in the editor
            fs.writeFileSync(solutionFilePath, solutionTemplate, { encoding: "utf8" });
            const document = await vscode.workspace.openTextDocument(solutionFilePath);
            await vscode.window.showTextDocument(document, vscode.ViewColumn.One);
    
            // Success message
            vscode.window.showInformationMessage(`Solution template created for ${problemName}!`);
        } catch (error) {
            console.error("Error in writeSolutionCommand:", error);
            vscode.window.showErrorMessage("An error occurred while creating the solution. Check the console for details.");
        }
    });
    
    // Command to run the solution
    const runSolutionCommand = vscode.commands.registerCommand('leetcode.runSolution', async () => {
        const solutionFileUri = await vscode.window.showOpenDialog({
            canSelectMany: false,
            openLabel: 'Select your solution file',
            filters: {
                Languages: ['py', 'cpp'],
            },
        });

        if (!solutionFileUri || solutionFileUri.length === 0) {
            vscode.window.showErrorMessage('No solution file selected!');
            return;
        }

        const solutionFile = solutionFileUri[0].fsPath;
        const language = solutionFile.endsWith('.py') ? 'python' : 'cpp';

        const testCaseDir = path.join(context.extensionPath, 'test_cases');
        if (!fs.existsSync(testCaseDir)) {
            vscode.window.showErrorMessage(`Test case directory does not exist: ${testCaseDir}`);
            return;
        }

        const scriptPath = path.join(context.extensionPath, 'src', 'compiler.py');
        const pythonCommand = 'python';
        const args = [scriptPath, language, solutionFile, testCaseDir];

        logMessage(outputChannel, `Executing command: ${pythonCommand} ${args.join(' ')}`);
        outputChannel.show();

        const compilerProcess = spawn(pythonCommand, args, { shell: true });

        compilerProcess.stdout.on('data', (data) => outputChannel.appendLine(data.toString()));
        compilerProcess.stderr.on('data', (data) => outputChannel.appendLine(`Error: ${data.toString()}`));

        compilerProcess.on('close', (code) => {
            if (code === 0) {
                vscode.window.showInformationMessage('Code executed successfully!');
                outputChannel.appendLine('Code executed successfully!');
            } else {
                vscode.window.showErrorMessage(`Compiler exited with code ${code}. Check the output channel for details.`);
                outputChannel.appendLine(`Compiler exited with code ${code}.`);
            }
        });
    });

    context.subscriptions.push(fetchTestCasesCommand, manageTestCasesCommand,writeSolutionCommand, runSolutionCommand);;
}


export function deactivate() {
    console.log('LeetForces Extension Deactivated');
}
