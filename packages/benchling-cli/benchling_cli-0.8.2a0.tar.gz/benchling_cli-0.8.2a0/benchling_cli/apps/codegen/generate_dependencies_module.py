from typing import Type, Union

from benchling_api_client.v2.beta.models.benchling_app_manifest import BenchlingAppManifest
from benchling_sdk.apps.config.scalars import JsonType, ScalarModelType
from benchling_sdk.apps.helpers.config_helpers import (
    app_config_type_from_dependency,
    element_definition_from_dependency,
    field_definitions_from_dependency,
    is_config_required,
    options_from_dependency,
    scalar_type_from_config,
    workflow_task_schema_output_from_dependency,
)
from jinja2 import Environment, PackageLoader

from benchling_cli.apps.codegen.helpers import (
    dependency_to_pascal_case,
    dependency_to_snake_case,
    is_manifest_scalar_dependency,
    is_secure_text_dependency,
    reformat_code_str,
)


def generate_dependencies_module(manifest: BenchlingAppManifest) -> str:
    env = Environment(
        loader=PackageLoader("benchling_cli.apps.codegen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("dependencies.py.jinja2")
    rendered_template = template.render(
        manifest=manifest,
        is_secure_text_dependency=is_secure_text_dependency,
        is_manifest_scalar_dependency=is_manifest_scalar_dependency,
        dependency_to_pascal_case=dependency_to_pascal_case,
        dependency_to_snake_case=dependency_to_snake_case,
        field_definitions_from_dependency=field_definitions_from_dependency,
        element_definition_from_dependency=element_definition_from_dependency,
        options_from_dependency=options_from_dependency,
        scalar_type_from_config=scalar_type_from_config,
        workflow_task_schema_output_from_dependency=workflow_task_schema_output_from_dependency,
        scalar_type_name=_scalar_type_name,
        is_config_required=is_config_required,
        app_config_type_from_dependency=app_config_type_from_dependency,
    )

    return reformat_code_str(rendered_template)


def _scalar_type_name(scalar_type: Union[object, Type[ScalarModelType]]) -> str:
    """Return the concrete type of scalar."""
    # from Python3.10, Union type have __name__ attribute returning 'Union".
    # We need to explicitly check for JsonType first.
    if scalar_type == JsonType:
        return "JsonType"

    if hasattr(scalar_type, "__name__"):
        return scalar_type.__name__  # type: ignore

    raise TypeError(f"{scalar_type} is not supported yet.")
