import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your ChromeDriver
CHROMEDRIVER_PATH = "C:\\chromedriver\\chromedriver-win64\\chromedriver.exe"

# Directory to store the test cases
TEST_CASES_DIR = "test_cases"

def clear_test_cases_directory():
    """Remove all files in the test_cases directory."""
    if os.path.exists(TEST_CASES_DIR):
        for file in os.listdir(TEST_CASES_DIR):
            file_path = os.path.join(TEST_CASES_DIR, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def fetch_and_store_test_cases(problem_url):
    """Fetch test cases from the LeetCode problem page."""
    clear_test_cases_directory()
    # Initialize WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        # Open the LeetCode problem URL
        driver.get(problem_url)

        # Wait for the page to load
        time.sleep(5)

        inputs, outputs = [],[]

        # Attempt to fetch test cases from <pre> tags
        try:
            problem_content = driver.find_elements(By.XPATH, "//pre")
            if problem_content:
                for content in problem_content:
                    case_text = content.text
                    parts = case_text.split("Output:")
                    if len(parts) == 2:
                        inputs.append(parts[0].strip().replace("Input: ", ""))
                        outputs.append(parts[1].split("\n")[0].strip())

        except Exception as e:
            print("Error while fetching from <pre> tags:", e)

        # If no inputs/outputs found, fall back to div structure
        if not inputs or not outputs:
            example_prefix_xpath = "//div/div[1]/div[3]/div/div"
            example_divs = driver.find_elements(By.XPATH, example_prefix_xpath)

            for div in example_divs:
                try:
                    input_element = div.find_element(By.XPATH, f".//p[1]")  # Input paragraph
                    output_element = div.find_element(By.XPATH, f".//p[2]")  # Output paragraph

                    inputs.append(input_element.text.strip().replace("Input: ", ""))
                    outputs.append(output_element.text.strip().replace("Output: ", ""))
                except Exception:
                    continue

        # If still no test cases are found, print an error
        if not inputs or not outputs:
            print("No test cases found!")
            return

        # Save test cases to files
        os.makedirs(TEST_CASES_DIR, exist_ok=True)

        for i, (input_data, output_data) in enumerate(zip(inputs, outputs), start=1):
            with open(os.path.join(TEST_CASES_DIR, f"input_{i}.txt"), "w") as input_file:
                input_file.write(input_data)
            with open(os.path.join(TEST_CASES_DIR, f"output_{i}.txt"), "w") as output_file:
                output_file.write(output_data)

        print(f"Test cases saved in '{TEST_CASES_DIR}' directory.")

    finally:
        driver.quit()

def view_test_cases():
    if not os.path.exists(TEST_CASES_DIR):
        print("No test cases found.")
        return

    print("\n--- Test Cases ---")
    for file_name in sorted(os.listdir(TEST_CASES_DIR)):
        with open(os.path.join(TEST_CASES_DIR, file_name), "r") as file:
            print(f"{file_name}:\n{file.read().strip()}")

def edit_test_case(file_name, new_content):
    file_path = os.path.join(TEST_CASES_DIR, file_name)
    if not os.path.exists(file_path):
        print("File not found.")
        return

    with open(file_path, "r") as file:
        print(f"Current content of {file_name}:\n{file.read().strip()}")
    with open(file_path, "w") as file:
        file.write(new_content)
    print(f"{file_name} updated.")

def add_test_case(input_data, output_data):
    os.makedirs(TEST_CASES_DIR, exist_ok=True)
    new_index = len(os.listdir(TEST_CASES_DIR)) // 2 + 1

    with open(os.path.join(TEST_CASES_DIR, f"input_{new_index}.txt"), "w") as input_file:
        input_file.write(input_data)
    with open(os.path.join(TEST_CASES_DIR, f"output_{new_index}.txt"), "w") as output_file:
        output_file.write(output_data)

    print(f"Added new test case: input_{new_index}.txt, output_{new_index}.txt")

def remove_test_case(index):
    input_file = os.path.join(TEST_CASES_DIR, f"input_{index}.txt")
    output_file = os.path.join(TEST_CASES_DIR, f"output_{index}.txt")

    if not (os.path.exists(input_file) and os.path.exists(output_file)):
        print(f"Test case {index} does not exist.")
        return

    os.remove(input_file)
    os.remove(output_file)
    print(f"Removed test case: input_{index}.txt, output_{index}.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch <url> | manage <subcommand>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "fetch" and len(sys.argv) > 2:
        fetch_and_store_test_cases(sys.argv[2])
    elif command == "manage":
        if len(sys.argv) < 3:
            print("Subcommand required: view, edit <file>, add <input> <output>, or remove <index>")
        elif sys.argv[2] == "view":
            view_test_cases()
        elif sys.argv[2] == "edit" and len(sys.argv) > 4:
            edit_test_case(sys.argv[3], sys.argv[4])
        elif sys.argv[2] == "add" and len(sys.argv) > 4:
            # Ensure that input and output arguments are provided
            try:
                input_data = sys.argv[3]
                output_data = sys.argv[4]
                add_test_case(input_data, output_data)
            except IndexError:
                print("Error: Both input and output data are required for adding a test case.")
        elif sys.argv[2] == "remove" and len(sys.argv) > 3:
            try:
                index = int(sys.argv[3])
                remove_test_case(index)
            except ValueError:
                print("Error: Please provide a valid test case index to remove.")
        else:
            print("Invalid manage subcommand.")
    else:
        print("Invalid command.")