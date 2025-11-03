import ast
from pathlib import Path
from typing import List, Dict

def write_unit_tests(results: List[Dict], tests_root: str = "tests"):
    """
    Create or update pytest test files in a mirrored 'tests/' directory.

    Automatically adapts to the project structure (no hardcoded 'src').

    Args:
        results (List[Dict]): List of LLM outputs with keys:
            - 'file_path': path to the source file
            - 'name': function name
            - 'test_code': pytest test code
            - 'imports' (optional): list of import lines to add
        tests_root (str, optional): Root test folder (default: 'tests').
    """
    tests_root = Path(tests_root)
    grouped = {}

    # Try to detect a common root (e.g., 'src', 'app', etc.)
    all_paths = [Path(item["file_path"]).resolve() for item in results]
    common_root = Path(*Path(all_paths[0]).parts[:1])
    for p in all_paths:
        for part in p.parts:
            if part in ("src", "app", "package"):
                common_root = Path(*p.parts[: p.parts.index(part) + 1])
                break

    for item in results:
        src_path = Path(item["file_path"]).resolve()

        try:
            rel_path = src_path.relative_to(common_root)
        except ValueError:
            rel_path = src_path.name

        test_path = tests_root / Path(rel_path).parent / f"test_{Path(rel_path).stem}.py"
        grouped.setdefault(test_path, []).append(item)

    for test_file, items in grouped.items():
        test_file.parent.mkdir(parents=True, exist_ok=True)
        text = test_file.read_text(encoding="utf-8") if test_file.exists() else ""

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

        # Ensure pytest import
        if not any("import pytest" in line for line in lines):
            header_lines.append("import pytest")

        # Ensure imports for each tested function
        for item in items:
            module_path = Path(item["file_path"]).with_suffix("").as_posix().replace("/", ".")
            import_line = f"from {module_path} import {item['name']}"
            if not any(import_line in line for line in lines):
                header_lines.append(import_line)

            for imp in item.get("imports", []):
                if not any(imp in line for line in lines):
                    header_lines.append(imp)

        if header_lines:
            lines = header_lines + [""] + lines

        for item in items:
            name = f"test_{item['name']}"
            code_lines = item["test_code"].strip().splitlines()

            if name in existing_funcs:
                start, end = existing_funcs[name]
                print(f"🔁 Replacing test '{name}' in {test_file}")
                lines[start:end] = code_lines
            else:
                print(f"➕ Adding test '{name}' to {test_file}")
                lines.extend(["", *code_lines])

        test_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        print(f"✅ Updated {test_file}")
