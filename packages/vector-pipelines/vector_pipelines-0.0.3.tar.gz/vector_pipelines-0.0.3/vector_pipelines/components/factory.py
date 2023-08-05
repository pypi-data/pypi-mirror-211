from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from vector_pipelines.components.service import Serviceable

_components = {}


def register_component(component_name: str) -> Callable[[type[Any]], type[Any]]:
    """Decorator for registering a component.

    Args:
        component_name: The name of the component to register.

    Returns:
        A decorator that registers the decorated class as a component.
    """

    def decorator(cls: type[Any]) -> type[Any]:
        _components[component_name] = cls
        return cls

    return decorator


def get_component(component_name: str) -> type[Serviceable]:
    """Gets the class of a component.

    Args:
        component_name: The name of the component to get.

    Returns:
        The class of the component.
    """
    return _components[component_name]
