import bisect
from collections import defaultdict, deque
import collections
import heapq
import math
import os
import random
import string
import sys
import ast
import subprocess
import shutil


def parse_input(file_path):
    """Parses the input file into a dictionary."""
    with open(file_path, "r") as f:
        content = f.read().strip()

    input_dict = {}
    assignments = content.split(", ")
    for assignment in assignments:
        key, value = assignment.split("=", 1)
        input_dict[key.strip()] = ast.literal_eval(value.strip())

    return input_dict


def execute_python(solution_file, inputs):
    """Executes Python solution."""
    try:
        # Read the solution file
        with open(solution_file, "r") as f:
            code = f.read()

        # Inject necessary imports into the execution context
        global_imports = {
            "string" : string,
            "collections": collections,
            "defaultdict": defaultdict,
            "deque": deque,
            "math": math,
            "bisect":bisect,
            "heapq":heapq,
            "random":random,

        ## ADD MORE IF REQUIRED ##
        }

        # Dynamically load the code and execute the `solve` function
        local_vars = {}
        exec(code, global_imports, local_vars)

        # Extract the Solution class and initialize it
        solution_class = local_vars.get("Solution")
        if not solution_class:
            print(f"Error: The solution file does not contain a `Solution` class.")
            return None

        solution = solution_class()

        # Ensure the solve method exists
        if not hasattr(solution, "solve"):
            print(f"Error: The `Solution` class does not contain a `solve` method.")
            return None

        # Execute the solve method with inputs
        return solution.solve(**inputs)

    except Exception as e:
        print(f"Runtime Error:\n{e}")
        return None


def execute_cpp(solution_file, processed_input):
    """Executes C++ solution."""
    if not shutil.which("g++"):
        print("Error: g++ compiler not found. Please ensure it's installed and in the system PATH.")
        return None

    exe_file = os.path.splitext(solution_file)[0] + ".exe"

    # Compile the C++ file
    compile_process = subprocess.run(
        ["g++", "-std=c++20", "-o", exe_file, solution_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if compile_process.returncode != 0:
        print(f"Compilation Error:\n{compile_process.stderr}")
        return None

    # Execute the compiled binary
    process = subprocess.run(
        [exe_file],
        input=processed_input,  # Pass input as stdin
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if process.returncode != 0:
        print(f"Runtime Error:\n{process.stderr.strip()}")
        return None

    return process.stdout.strip()


def execute_code(language, solution_file, test_case_dir):
    """Executes the solution file against test cases."""
    input_files = sorted(
        [f for f in os.listdir(test_case_dir) if f.startswith("input_")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )
    output_files = sorted(
        [f for f in os.listdir(test_case_dir) if f.startswith("output_")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )

    for i, (input_file, output_file) in enumerate(zip(input_files, output_files)):
        input_path = os.path.join(test_case_dir, input_file)
        output_path = os.path.join(test_case_dir, output_file)

        inputs = parse_input(input_path)
        with open(output_path, "r") as f:
            expected_output = f.read().strip()

        print(f"--- Test Case {i + 1} ---")
        if language == "python":
            try:
        # Execute Python solution and compare output
                result = execute_python(solution_file, inputs)
                #print(result)

                if result is None:
                    print("Execution failed.")
                else:
                    if isinstance(result,bool):
                        result_obj = "true" if result else "false"
                        #print(result_obj)
            # If result is a list, no need to strip
                    elif isinstance(result, (list,dict)):
                        result_obj = result  # No need to split or strip
                    elif isinstance(result, int):
                        result_obj = result
                    else:
                # For string results, you can strip and process
                        result_obj = str(result).strip()
                #print(result_obj)
                        

                try :
                    expected_output_obj = ast.literal_eval(expected_output)
                except Exception:
                    expected_output_obj = expected_output.strip()
                #print(expected_output_obj)

                if expected_output_obj == result_obj:
                    print("Test Case PASSED")
                else:
                    print("Test Case FAILED")
                    print(f"Expected: {expected_output_obj}")
                    print(f"Actual: {result_obj}")

            except Exception as e:
                print("Test Case FAILED")
                print(f"Error executing Python solution: {e}")
                print(f"Raw Expected: {expected_output}")
                print(f"Raw Actual: {result}")


        elif language == "cpp":
            try:
                #print(inputs)
                #print(expected_output)

                # Prepare the processed input string for C++ stdin
                # Prepare the processed input string for C++ stdin
                processed_input = ""
                input_values = list(inputs.values())  # Convert dict_values to a list
                for i in range(len(input_values)):
                    value = input_values[i]
                    input_i = ""
    
                    if isinstance(value, list):
        # Check if it is a list of lists (vector<vector<int>>)
                        if all(isinstance(item, list) for item in value):
            # For nested lists, print each sublist on a new line
                            for sublist in value:
                                if sublist :
                                    input_i += " ".join(str(v) for v in sublist) + "\n"
                                else :
                                    input_i += "0\n"
                        else:
            # Regular list processing (vector<int>)
                            if value :
                                input_i += " ".join(str(v) for v in value)
                            else :
                                input_i += ""
                    else:
                        input_i += str(value)
    
    # Add the processed input to the overall string
                    if i == len(input_values) - 1:  # Last element, no newline
                        processed_input += input_i
                    else:
                        processed_input += input_i + "\n"

# Print the processed input for debugging
                #print(processed_input)

# Execute C++ solution and compare output
                result = execute_cpp(solution_file, processed_input)


                if result is None:
                    print("Execution failed.")
                else:
                    try :
                        expected_output_obj = ast.literal_eval(expected_output)
                    except Exception :
                        expected_output_obj = expected_output.strip()
                        if expected_output_obj == "true" :
                            expected_output_obj = True
                        elif expected_output_obj == "false":
                            expected_output_obj = False
                    if isinstance(expected_output_obj,bool):
                        expected_output_obj = "1" if expected_output_obj else "0"
                        #print("yeah its a bool")
                    print(expected_output_obj)
                    if isinstance(expected_output_obj, list):
                        if all(isinstance(item,list) and all(isinstance(subitem,int) for subitem in item) for item in expected_output_obj):
                            expected_output_obj = "\n".join(" ".join(str(v) for v in sublist) for sublist in expected_output_obj)
                        elif all(isinstance(item, list) and all(isinstance(subitem, str) for subitem in item) for item in expected_output_obj):
                            expected_output_obj = "\n".join(
            " ".join(f"\"{v}\"" for v in sublist) for sublist in expected_output_obj
        )
                        else :
                            expected_output_obj = " ".join(str(i) for i in expected_output_obj)
                    if isinstance(result, (list,dict)):
                        if all(isinstance(item,list) for item in result):
                            result_obj = "\n".join(" ".join(str(v) for v in sublist) for sublist in result)
                            #print("i am here")
                        else :
                            result_obj = result 
                        #print("i am if") # No need to split or strip
                    else:
                # For string results, you can strip and process
                        result_obj = str(result).strip()
                        #print("i am else")
                    #print(result_obj)
                    if isinstance(expected_output_obj, str) and "\n" in expected_output_obj:
    # Transform result_obj string into multiline string format
    # Strip the outer brackets and split into sublists
                        result_obj = result_obj.strip("[]").split("] [")
    
    # Normalize each sublist
                        result_obj = [" ".join(sublist.strip("[]").split()) for sublist in result_obj]
    
    # Join sublists with newline
                        result_obj = "\n".join(result_obj)
                        #print(result_obj)
                    elif isinstance(expected_output_obj,str) and "\n" not in expected_output_obj:
                        result_obj = result_obj.strip("[]")


                    if str(expected_output_obj).strip() == str(result_obj).strip():
                        print("Test Case PASSED")
                    else:
                        print("Test Case FAILED")
                        print(f"Expected: {expected_output_obj}")
                        print(f"Actual: {result_obj}")

            except Exception as e:
                print("Test Case FAILED")
                print(f"Error executing C++ solution: {e}")
                print(f"Raw Expected: {expected_output}")
                print(f"Raw Actual: {result}")

        else:
            print("Unsupported language!")
            return



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python compiler.py <language> <solution_file> <test_case_dir>")
        sys.exit(1)

    language = sys.argv[1]
    solution_file = sys.argv[2]
    test_case_dir = sys.argv[3]

    execute_code(language, solution_file, test_case_dir)
