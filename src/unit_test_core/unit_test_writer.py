import ast
from pathlib import Path
from typing import List, Dict
from collections import defaultdict


def write_unit_tests(
    results: List[Dict],
    project_path: str,
    tests_root: str = "tests"
):
    """
    Create or update pytest test files in a mirrored 'tests/' directory.

    This version:
    - Rewrites the file entirely (no leftover duplicates).
    - Normalizes imports: merges `from a import b` and `from a import b,c`.
    - Ensures essential imports (pytest, Path) are present.
    - Avoids duplicate imports.

    Args:
        results (List[Dict]): List of LLM-generated outputs containing:
            - 'file_path': Path to the source file.
            - 'name': Function name to test.
            - 'test_code': Pytest test code as a string.
            - 'imports' (optional): List of import lines to include.
        project_path (str): Root path of the project.
        tests_root (str, optional): Root folder for tests (default: 'tests').
    """
    project_path = Path(project_path).resolve()
    tests_root = Path(tests_root)
    grouped = defaultdict(list)

    # Group items by test file path
    for item in results:
        src_path = Path(item["file_path"]).resolve()
        try:
            rel_path = src_path.relative_to(project_path)
        except ValueError:
            rel_path = src_path.name

        test_file = tests_root / rel_path.parent / f"test_{rel_path.stem}.py"
        grouped[test_file].append(item)

    # Helper to normalize imports
    def normalize_imports(import_lines: List[str]) -> List[str]:
        import_map = defaultdict(set)  # module -> set of names
        raw_imports = set()
        for line in import_lines:
            line = line.strip()
            if line.startswith("import "):
                raw_imports.add(line)
            elif line.startswith("from "):
                parts = line.split()
                module = parts[1]
                names = parts[3].split(",")
                for n in names:
                    import_map[module].add(n.strip())
        normalized = list(raw_imports)
        for module, names in import_map.items():
            normalized.append(f"from {module} import {', '.join(sorted(names))}")
        return sorted(normalized)

    # Process each test file
    for test_file, items in grouped.items():
        test_file.parent.mkdir(parents=True, exist_ok=True)
        lines = []

        # Collect all imports from items
        all_imports = set()
        for item in items:
            for imp in item.get("imports", []):
                all_imports.add(imp.strip())
        # Ensure essential imports
        all_imports.add("import pytest")
        all_imports.add("from pathlib import Path")

        # Normalize and merge
        final_imports = normalize_imports(list(all_imports))
        lines.extend(final_imports)
        lines.append("")  # blank line after imports

        # Add all test functions
        for item in items:
            code_lines = item["test_code"].strip().splitlines()
            lines.extend(code_lines)
            lines.append("")  # blank line between functions

        # Write the final file (overwrite)
        test_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"✅ Updated {test_file}")
