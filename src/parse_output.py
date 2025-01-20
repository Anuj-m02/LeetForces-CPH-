import sys
import json
import ast
import re

def infer_output_type(value):
    """Infer type for the value."""
    if isinstance(value, list):
        if all(isinstance(item, (int, float)) for item in value):
            return "vector<int>"
        if all(isinstance(item, list) or isinstance(item, int) for item in value):
            if all(
                isinstance(item, int) or 
                (isinstance(item, list) and all(isinstance(subitem, int) for subitem in item))
                for item in value
            ):
                return "vector<vector<int>>"
        if all(isinstance(item, list) and all(isinstance(subitem,str) for subitem in item)
                 for item in value
                 ):
            return "vector<vector<string>>"
        elif all(isinstance(item,str) and len(item) == 1 and item.isalpha() for item in value):
            return "vector<char>"
        elif all(isinstance(item, str) for item in value):
            return "vector<string>"
        return "vector<any>"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, str):
        return "string"
    return "any"  # For unsupported or unknown types

def parse_output_file(output_file):
    try:
        with open(output_file, 'r') as file:
            data = file.read().strip()
            
            # Use regex to replace standalone "true" and "false"
            data = re.sub(r'\btrue\b', 'True', data)
            data = re.sub(r'\bfalse\b', 'False', data)
            
            # Safely evaluate the output
            try:
                parsed_data = ast.literal_eval(data)
                output_type = infer_output_type(parsed_data)
                return {"type": output_type, "value": parsed_data}
            except Exception:
                raise ValueError(f"Invalid output format: {data}")
    except Exception as e:
        print(f"Error parsing output file: {e}", file=sys.stderr)
        return {}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_output.py <output_file>")
        sys.exit(1)
    
    output_file = sys.argv[1]
    result = parse_output_file(output_file)
    if not result:
        print("Failed to parse the output file.")
    else:
        print(json.dumps(result))
