from pathlib import Path
from typing import List, Dict
from collections import defaultdict
from src.unit_test_core.fixer_agent import UnitTestFixerAgent  # Custom LLM agent

SYSTEM_PROMPT_FIXER = """
You are an expert Python developer and pytest specialist. 
Your task is to review and correct Python test code files. 
Ensure that:
- The code is valid and directly runnable with pytest.
- All necessary imports are included and normalized in the top of the file (no duplicates).
- Test functions are syntactically correct and complete.
- Common mistakes are fixed (assertions, function calls, etc.).
- The overall style is clean and readable.

Output the entire corrected Python file as a string. Do not add explanations or markdown.
"""

class UnitTestWriterWithReview:
    """
    Writes pytest test files for a project and optionally reviews the code
    using an LLM agent before writing.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.fixer_agent = UnitTestFixerAgent(name="unit_test_fixer",
                                              model_name=model_name, 
                                              system_prompt=SYSTEM_PROMPT_FIXER)

    @staticmethod
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

    async def _review_code(self, code: str, project_path: str, original_path: str) -> str:
        """
        Pass the full test file content to the agent for review and correction.
        """
        corrected_code = await self.fixer_agent.fix_tests(code, str(project_path), str(original_path))
        return corrected_code

    async def write_unit_tests(
        self,
        results: List[Dict],
        project_path: str,
        tests_root: str = "tests",
        review: bool = True
    ):
        """
        Create or update pytest test files in a mirrored 'tests/' directory.
        Optionally review and fix the code using an LLM agent.
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

        # Process each test file
        for test_file, items in grouped.items():
            orig_path = items[0]['file_path']
            test_file.parent.mkdir(parents=True, exist_ok=True)
            lines = []

            # Collect all imports from items
            all_imports = set()
            for item in items:
                for imp in item.get("imports", []):
                    all_imports.add(imp.strip())

            # Normalize and merge
            final_imports = self.normalize_imports(list(all_imports))
            lines.extend(final_imports)
            lines.append("")  # blank line after imports

            # Add all test functions
            for item in items:
                code_lines = item["test_code"].strip().splitlines()
                lines.extend(code_lines)
                lines.append("")  # blank line between functions

            # Combine into single string
            full_file_code = "\n".join(lines).rstrip() + "\n"

            # Review and fix the code using the agent if requested
            if review:
                full_file_code = await self._review_code(full_file_code, str(project_path), str(orig_path))

            # Write the final file (overwrite)
            test_file.write_text(full_file_code, encoding="utf-8")
            print(f"✅ Updated {test_file}")

# Usage example (async context):
# writer = UnitTestWriterWithReview(model_name="gpt-4o-mini")
# await writer.write_unit_tests(results, project_path="C:/Users/.../project")
