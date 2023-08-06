from __future__ import annotations

"""
https://github.com/lidatong/dataclasses-json/
https://github.com/Fatal1ty/mashumaro

https://github.com/horejsek/python-fastjsonschema
https://github.com/s-knibbs/dataclasses-jsonschema
https://github.com/marshmallow-code/apispec
https://github.com/strongbugman/apiman

starlette.starlette.schemas.BaseSchemaGenerator
"""

import sys
from collections.abc import Callable
from inspect import Parameter
from inspect import signature
from inspect import Signature
from typing import Any
from typing import cast
from typing import ForwardRef

# from pydantic.typing
if sys.version_info < (3, 9):

    def evaluate_forwardref(
        type_: ForwardRef, globalns: Any, localns: Any
    ) -> Any:
        return type_._evaluate(globalns, localns)

else:

    def evaluate_forwardref(
        type_: ForwardRef, globalns: Any, localns: Any
    ) -> Any:
        # Even though it is the right signature for python 3.9,
        #  mypy complains with `error: Too many arguments for
        #  "_evaluate" of "ForwardRef"` hence the cast...
        return cast(Any, type_)._evaluate(globalns, localns, set())


# from fastapi.dependencies.utils
def get_typed_annotation(param: Parameter, globalns: dict[str, Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


# from fastapi.dependencies.utils
def get_typed_signature(call: Callable[..., Any]) -> Signature:
    signature_ = signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature_.parameters.values()
    ]
    typed_signature = Signature(typed_params)
    return typed_signature


def openapi_scheme(  # noqa
    self,
    title: str,
    version: str,
    routes: Sequence["BaseRoute"],
    openapi_version: str = "3.0.2",
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    servers: list[dict[str, str | Any]] | None = None,
    terms_of_service: str | None = None,
    contact: dict[str, str | Any] | None = None,
    license_info: dict[str, str | Any] | None = None,
) -> bytes:
    info: dict[str, Any] = {"title": title, "version": version}
    if description:
        info["description"] = description
    if terms_of_service:
        info["termsOfService"] = terms_of_service
    if contact:
        info["contact"] = contact
    if license_info:
        info["license"] = license_info
    output: dict[str, Any] = {"openapi": openapi_version, "info": info}
    if servers:
        output["servers"] = servers
    components: dict[str, dict[str, Any]] = {}
    paths: dict[str, dict[str, Any]] = {}
    operation_ids: set[str] = set()
    flat_models = get_flat_models_from_routes(routes)
    model_name_map = get_model_name_map(flat_models)
    definitions = get_model_definitions(
        flat_models=flat_models, model_name_map=model_name_map
    )
    for route in routes:
        # if isinstance(route, routing.APIRoute):
        result = get_openapi_path(
            route=route,
            model_name_map=model_name_map,
            operation_ids=operation_ids,
        )
        if result:
            path, security_schemes, path_definitions = result
            if path:
                paths.setdefault(route.path_format, {}).update(path)
            if security_schemes:
                components.setdefault("securitySchemes", {}).update(
                    security_schemes
                )
            if path_definitions:
                definitions.update(path_definitions)
    if definitions:
        components["schemas"] = {k: definitions[k] for k in sorted(definitions)}
    if components:
        output["components"] = components
    output["paths"] = paths
    if tags:
        output["tags"] = tags
    return JsonSerializer().serialize(output)
