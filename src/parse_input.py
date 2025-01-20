import sys
import ast
import json

def infer_type(value):
    """Infer type for the value."""
    if isinstance(value, list):
        if all(isinstance(item, (int, float)) for item in value):
            return "vector<int>"
        # Handle mixed lists like [1, [2], 3]
        if all(
            isinstance(item, list) or isinstance(item, int)
            for item in value
        ):
            # Check if all sublist elements are integers when they are lists
            if all(
                isinstance(item, int) or 
                (isinstance(item, list) and all(isinstance(subitem, int) for subitem in item))
                for item in value
            ) and not (all(isinstance(item, (int, float)) for item in value)):
                return "vector<vector<int>>"
        #elif all(isinstance(item, (int, float)) for item in value):  # Check if list contains numbers
         #   return "vector<int>"
        elif all(isinstance(item, list) and all(isinstance(subitem,str) for subitem in item)
                 for item in value
                 ):
            return "vector<vector<string>>"
        elif all(isinstance(item,str) and len(item) == 1 and item.isalpha() for item in value):
            return "vector<char>"
        elif all(isinstance(item, str) for item in value):  # Check if list contains strings
            return "vector<string>"
        return "vector<any>"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, str):
        return "string"
    return "any"  # For unsupported or unknown types


def parse_input(file_path):
    """Parse input file and extract arguments, keys, and types."""
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()

        if not content:
            raise ValueError("Input file is empty.")

        input_dict = {}
        for line in content.split(", "):  # Split based on your expected format
            if '=' not in line:
                raise ValueError(f"Invalid input format: '{line}' (missing '=')")

            key, value = line.split('=', 1)  # Split only on the first '='
            key = key.strip()
            value = value.strip()

            # Safely evaluate the value (e.g., for lists, dictionaries, etc.)
            input_dict[key] = ast.literal_eval(value)

        keys = list(input_dict.keys())
        types = [infer_type(value) for value in input_dict.values()]

        return keys, types, input_dict

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ValueError: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse.py <input_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        keys, types, values = parse_input(input_file)
        # Output the keys, types, and values as a JSON string
        output = {
            "keys": keys,
            "types": types,
            "values": values
        }
        print(json.dumps(output))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
