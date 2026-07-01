"""Template rendering service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from autoinvo.templates.contracts import (
    TemplateData,
    TemplateRenderOptions,
    TemplateRenderer,
)


@dataclass(frozen=True)
class JinjaTemplateConfig:
    """Default configuration for Jinja-based template rendering."""

    template_dir: str | Path = Path("templates")
    autoescape: bool = True


class JinjaTemplateRenderer(TemplateRenderer):
    """Render templates to HTML using Jinja2."""

    def __init__(self, config: JinjaTemplateConfig | None = None) -> None:
        self._config = config or JinjaTemplateConfig()

    def _build_environment(self, options: TemplateRenderOptions | None = None) -> Environment:
        template_dir = (options.template_dir if options and options.template_dir is not None else self._config.template_dir)
        strict_variables = options.strict_variables if options else False

        undefined_cls: type[Any] = StrictUndefined if strict_variables else type(None)

        if strict_variables:
            environment = Environment(
                loader=FileSystemLoader(str(template_dir)),
                autoescape=self._config.autoescape,
                undefined=StrictUndefined,
            )
        else:
            environment = Environment(
                loader=FileSystemLoader(str(template_dir)),
                autoescape=self._config.autoescape,
            )

        return environment

    def render(
        self,
        template_name: str,
        data: TemplateData,
        options: TemplateRenderOptions | None = None,
    ) -> str:
        environment = self._build_environment(options)
        template = environment.get_template(template_name)
        return template.render(**data)