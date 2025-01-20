import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess

# Define constants
TEST_CASES_DIR = "test_cases"
SCRIPT_PATH = "fetch_test_cases.py"

# Create the main GUI application
class LeetForcesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LeetForces GUI")
        self.root.geometry("600x400")
        
        # URL Input
        tk.Label(root, text="LeetCode Problem URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        
        # Fetch Test Cases Button
        self.fetch_button = tk.Button(root, text="Fetch Test Cases", command=self.fetch_test_cases)
        self.fetch_button.pack(pady=5)
        
        # View Test Cases Button
        self.view_button = tk.Button(root, text="View Test Cases", command=self.view_test_cases)
        self.view_button.pack(pady=5)
        
        # Add Test Case Section
        tk.Label(root, text="Add Test Case").pack(pady=5)
        self.input_data = tk.Entry(root, width=30)
        self.input_data.pack(pady=2)
        self.output_data = tk.Entry(root, width=30)
        self.output_data.pack(pady=2)
        self.add_button = tk.Button(root, text="Add Test Case", command=self.add_test_case)
        self.add_button.pack(pady=5)

        # Log/Output Area
        tk.Label(root, text="Logs:").pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=10)
        self.log_area.pack(pady=5)

    # Fetch Test Cases
    def fetch_test_cases(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        
        self.clear_test_cases_directory()
        self.log_area.insert(tk.END, f"Fetching test cases for URL: {url}\n")
        
        try:
            subprocess.run(["python", SCRIPT_PATH, "fetch", url], check=True)
            self.log_area.insert(tk.END, "Test cases fetched successfully.\n")
        except Exception as e:
            self.log_area.insert(tk.END, f"Error fetching test cases: {e}\n")
    
    # View Test Cases
    def view_test_cases(self):
        if not os.path.exists(TEST_CASES_DIR):
            messagebox.showerror("Error", "No test cases found.")
            return
        
        self.log_area.insert(tk.END, "--- Test Cases ---\n")
        for file_name in sorted(os.listdir(TEST_CASES_DIR)):
            with open(os.path.join(TEST_CASES_DIR, file_name), "r") as file:
                self.log_area.insert(tk.END, f"{file_name}:\n{file.read().strip()}\n")
        self.log_area.insert(tk.END, "-------------------\n")
    
    # Add Test Case
    def add_test_case(self):
        input_data = self.input_data.get()
        output_data = self.output_data.get()
        if not input_data or not output_data:
            messagebox.showerror("Error", "Both input and output are required.")
            return
        
        try:
            subprocess.run(["python", SCRIPT_PATH, "manage", "add", input_data, output_data], check=True)
            self.log_area.insert(tk.END, "Test case added successfully.\n")
        except Exception as e:
            self.log_area.insert(tk.END, f"Error adding test case: {e}\n")
    
    # Clear Test Cases Directory
    def clear_test_cases_directory(self):
        if os.path.exists(TEST_CASES_DIR):
            for file in os.listdir(TEST_CASES_DIR):
                os.remove(os.path.join(TEST_CASES_DIR, file))
            self.log_area.insert(tk.END, "Cleared old test cases.\n")

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = LeetForcesApp(root)
    root.mainloop()
