from src.unit_test_core.unit_test_executor import execute_unit_test_in_path


# ============================================================
#  Unit Test Generation Core
# ============================================================

async def gradio_generate_unit_tests(folder_path, model, names="", project_path=None):
    """Gradio handler for test generation using executor (archivo por archivo)."""
    if not project_path:
        return "❌ Please provide the project root path (required)."

    target_names = [n.strip() for n in names.split(",")] if names else None

    await execute_unit_test_in_path(
        path=folder_path,
        model_name=model,
        target_names=target_names,
        project_path=project_path,
    )

    return "✅ Unit tests generated and written to 'tests/' folder."

