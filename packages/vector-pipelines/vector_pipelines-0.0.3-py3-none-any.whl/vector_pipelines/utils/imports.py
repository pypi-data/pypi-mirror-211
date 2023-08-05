from __future__ import annotations

import importlib.util


def _check_module_is_available(module_name: str) -> bool:
    """Checks if a module is available.

    Args:
        module_name: The name of the module to check.

    Returns:
        `True` if the module is available, `False` otherwise.
    """
    return importlib.util.find_spec(module_name) is not None


_SENTENCE_TRANSFORMERS_AVAILABLE = _check_module_is_available("sentence_transformers")
