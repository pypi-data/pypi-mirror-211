from __future__ import annotations

import typer

from vector_pipelines.components.factory import get_component

app = typer.Typer()


def parse_extra_args(
    args: list[str], expected_attributes: list[str], component_name: str
) -> dict[str, str]:
    """Parses extra arguments from the command line.

    Args:
        args: The list of extra arguments.
        expected_attributes: The list of expected attributes.
        component_name: The name of the component.

    Returns:
        A dictionary of the extra arguments.
    """
    kwargs = {}
    for arg in args:
        if "=" not in arg:
            raise ValueError(f"Invalid argument: {arg}. Expected format: --key=value")
        key, value = arg.split("=")
        key = key.replace("--", "")
        if key not in expected_attributes:
            expected_attributes_str = ", ".join(
                [f"'{attr}'" for attr in expected_attributes]
            )
            raise ValueError(
                f"Invalid argument: '{key}'. Expected one of"
                f" {expected_attributes_str} for '{component_name}' component."
            )
        kwargs[key] = value
    return kwargs


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def start(
    ctx: typer.Context,
    component_name: str = typer.Option(
        None, help="The name of the component to serve."
    ),
    port: int = typer.Option(
        50051,
        help="The port to serve the component on.",
    ),
) -> None:
    """Starts a service for serving a component."""
    Component = get_component(component_name)
    components_kwargs = parse_extra_args(
        args=ctx.args,
        expected_attributes=list(Component.config_cls.__annotations__.keys()),
        component_name=component_name,
    )
    component = Component(**components_kwargs)
    component.serve(port=port)
