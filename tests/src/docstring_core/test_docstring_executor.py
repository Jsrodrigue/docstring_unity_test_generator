from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_docstring_writer_wrapper_calls_write_docstrings():
    dummy_path = Path("/tmp/fake.py")
    items = [{"name": "func", "docstring": "doc"}]
    with patch(
        "src.docstring_core.docstring_executor.write_docstrings",
        new_callable=AsyncMock,
    ) as mock_write:
        from src.docstring_core.docstring_executor import _docstring_writer_wrapper

        await _docstring_writer_wrapper(dummy_path, items, extra="ignored")
        mock_write.assert_awaited_once_with(dummy_path, items)


@pytest.mark.asyncio
async def test_docstring_writer_wrapper_empty_items():
    dummy_path = Path("/tmp/fake2.py")
    items = []
    with patch(
        "src.docstring_core.docstring_executor.write_docstrings",
        new_callable=AsyncMock,
    ) as mock_write:
        from src.docstring_core.docstring_executor import _docstring_writer_wrapper

        await _docstring_writer_wrapper(dummy_path, items)
        mock_write.assert_awaited_once_with(dummy_path, items)


def test_execute_docstring_in_path_calls_execute_in_path_with_defaults():
    called_args = {}

    async def fake_execute_in_path(**kwargs):
        called_args.update(kwargs)

    with patch(
        "src.docstring_core.docstring_executor.execute_in_path",
        new=fake_execute_in_path,
    ):
        from src.docstring_core.docstring_executor import (
            execute_docstring_in_path,
            _docstring_writer_wrapper,
            generate_docstring_from_path_dict,
        )

        execute_docstring_in_path(path="my/path")

    assert called_args["path"] == "my/path"
    assert called_args["model_name"] == "gpt-4o-mini"
    assert called_args["target_names"] is None
    assert called_args["project_path"] is None
    assert called_args["generate_func"] is generate_docstring_from_path_dict
    assert called_args["write_func"] is _docstring_writer_wrapper
    assert called_args["item_name"] == "docstrings"


def test_execute_docstring_in_path_custom_arguments():
    called_args = {}

    async def fake_execute_in_path(**kwargs):
        called_args.update(kwargs)

    with patch(
        "src.docstring_core.docstring_executor.execute_in_path",
        new=fake_execute_in_path,
    ):
        from src.docstring_core.docstring_executor import (
            execute_docstring_in_path,
            _docstring_writer_wrapper,
            generate_docstring_from_path_dict,
        )

        execute_docstring_in_path(
            path="custom/path",
            model_name="custom-model",
            target_names=["a", "b"],
            project_path="/proj",
        )

    assert called_args["path"] == "custom/path"
    assert called_args["model_name"] == "custom-model"
    assert called_args["target_names"] == ["a", "b"]
    assert called_args["project_path"] == "/proj"
    assert called_args["generate_func"] is generate_docstring_from_path_dict
    assert called_args["write_func"] is _docstring_writer_wrapper
    assert called_args["item_name"] == "docstrings"
