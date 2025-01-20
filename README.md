# leetforces README

This is the README for your extension "leetforces". After writing up a brief description, we recommend including the following sections.

LeetForces
LeetForces is a VSCode extension designed to help users fetch, manage, and test LeetCode problems using Python or C++. The extension allows users to fetch test cases from LeetCode by URL, store them in a designated folder, and run their solutions against these test cases.

Project Description
LeetForces fetches test cases from LeetCode through the problem URL and stores them in the test cases folder. Afterward, you can write and run Python or C++ solutions against the fetched inputs, compare expected and actual outputs, and refine your solutions accordingly. 

## Features

Describe specific features of your extension including screenshots of your extension in action. Image paths are relative to this README file.

For example if there is an image subfolder under your extension project workspace:

\!\[feature X\]\(images/feature-x.png\)

> Tip: Many popular extensions utilize animations. This is an excellent way to show off your extension! We recommend short, focused animations that are easy to follow.

Usage
Fetch Test Cases
Run the fetch command to fetch test cases from a LeetCode problem by entering the problem URL.
The test cases will be stored in the test_cases folder.
Manage Test Cases
Use the manage command to edit, view, add, or remove test cases.
Write Solution
Use the write solution command to write your solution in either Python or C++.
The solution will be written under the appropriate template in the respective file.
Run Solution
Run your solution using the run solution command.
The command will execute your solution against the fetched test cases and show the expected and actual outputs for comparison.

## Requirements

If you have any requirements or dependencies, add a section describing those and how to install and configure them.

Installation Instructions
Before you begin, make sure to have the following installed:

Python (latest version)
C++ Compiler (such as GCC or Clang)
Required Python Modules:
ast
selenium
(Other modules as required, list them here)
NPM Packages:
(List all NPM packages required here)
Chromedriver (for Selenium)

## Extension Settings

Include if your extension adds any VS Code settings through the `contributes.configuration` extension point.

For example:

This extension contributes the following settings:

* `myExtension.enable`: Enable/disable this extension.
* `myExtension.thing`: Set to `blah` to do something.

## Known Issues

Calling out known issues can help limit users opening duplicate issues against your extension.

## Release Notes

Users appreciate release notes as you update your extension.

### 1.0.0

Initial release of ...

### 1.0.1

Fixed issue #.

### 1.1.0

Added features X, Y, and Z.

---

## Following extension guidelines

Ensure that you've read through the extensions guidelines and follow the best practices for creating your extension.

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

## Working with Markdown

You can author your README using Visual Studio Code. Here are some useful editor keyboard shortcuts:

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux).
* Toggle preview (`Shift+Cmd+V` on macOS or `Shift+Ctrl+V` on Windows and Linux).
* Press `Ctrl+Space` (Windows, Linux, macOS) to see a list of Markdown snippets.

## For more information

* [Visual Studio Code's Markdown Support](http://code.visualstudio.com/docs/languages/markdown)
* [Markdown Syntax Reference](https://help.github.com/articles/markdown-basics/)

**Enjoy!**
