import ast
from pathlib import Path
from typing import List, Dict

def write_unit_tests(results: List[Dict], tests_root: str = "tests"):
    """
    Create or update pytest test files in a mirrored 'tests/' directory.

    - Each src file gets a corresponding test file.
    - Existing tests for the same function are replaced.
    - Missing imports (pytest, function imports, and custom imports) are added automatically at the top.

    Args:
        results (List[Dict]): List of LLM outputs with keys:
            - 'file_path': path to the source file
            - 'name': name of the function being tested
            - 'test_code': pytest test code
            - 'imports' (optional): List of import lines to add
        tests_root (str, optional): Root test folder (default: 'tests').
    """
    tests_root = Path(tests_root)
    grouped = {}

    # Group test outputs by their corresponding test file
    for item in results:
        src_path = Path(item["file_path"]).resolve()
        try:
            rel_path = src_path.relative_to("src")
        except ValueError:
            rel_path = Path(src_path.name)  # fallback as Path

        test_path = tests_root / rel_path.parent / f"test_{rel_path.stem}.py"
        grouped.setdefault(test_path, []).append(item)

    for test_file, items in grouped.items():
        test_file.parent.mkdir(parents=True, exist_ok=True)

        if test_file.exists():
            text = test_file.read_text(encoding="utf-8")
        else:
            text = ""

        try:
            tree = ast.parse(text or "")
        except SyntaxError:
            print(f"⚠️ Could not parse {test_file}, overwriting.")
            tree = ast.parse("")

        existing_funcs = {
            node.name: (node.lineno - 1, getattr(node, "end_lineno", node.lineno))
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        lines = text.splitlines() if text else []
        header_lines = []

        # --- Ensure pytest import ---
        if not any("import pytest" in line for line in lines):
            header_lines.append("import pytest")

        # --- Ensure imports for each tested function and custom imports ---
        for item in items:
            module_path = (
                Path(item["file_path"])
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )
            import_line = f"from {module_path} import {item['name']}"
            if not any(import_line in line for line in lines):
                header_lines.append(import_line)

            # Custom imports for this test (optional)
            for imp in item.get("imports", []):
                if not any(imp in line for line in lines):
                    header_lines.append(imp)

        # Prepend imports if needed
        if header_lines:
            lines = header_lines + [""] + lines

        # --- Write or replace tests ---
        for item in items:
            name = f"test_{item['name']}"
            code = item["test_code"].strip()
            code_lines = code.splitlines()

            if name in existing_funcs:
                start, end = existing_funcs[name]
                print(f"🔁 Replacing test '{name}' in {test_file}")
                lines[start:end] = code_lines
            else:
                print(f"➕ Adding test '{name}' to {test_file}")
                if not lines or not lines[-1].strip():
                    lines.extend(code_lines)
                else:
                    lines.extend(["", *code_lines])

        test_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        print(f"✅ Updated {test_file}")


# -----------------------------
# Quick test with 2 functions
# -----------------------------
if __name__ == "__main__":
    dummy_results = [
        {
            "file_path": "src/docstring_core/docstring_scanner.py",
            "name": "scan_folder_for_docstrings",
            "test_code": """
def test_scan_folder_for_docstrings():
    assert True
""",
            "imports": ["from unittest.mock import patch, MagicMock"]
        },
        {
            "file_path": "src/docstring_core/docstring_scanner.py",
            "name": "another_function",
            "test_code": """
def test_another_function():
    assert 1 + 1 == 2
""",
            "imports": ["from unittest.mock import patch"]
        }
    ]

    print("🧪 Running write_unit_tests with dummy data...")
    write_unit_tests(dummy_results)
    print("✅ Done! Check the 'tests/docstring_core/test_docstring_scanner.py' file.")
