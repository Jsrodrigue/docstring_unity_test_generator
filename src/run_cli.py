from parser import extract_functions
from llm_client import generate_docstring
from cli_helper import compare_and_confirm, update_docstring_in_file

file_path = input("Enter Python file path: ")

functions = extract_functions(file_path)

for func in functions:
    suggested = generate_docstring(func)
    if compare_and_confirm(func, suggested):
        update_docstring_in_file(file_path, func['name'], suggested)
        print(f"Docstring updated for {func['name']}")
    else:
        print(f"Docstring skipped for {func['name']}")
