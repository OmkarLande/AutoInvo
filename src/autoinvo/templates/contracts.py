"""Contracts for template rendering."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from dataclasses import dataclass


TemplateData = dict[str, Any]


@dataclass(frozen=True)
class TemplateRenderOptions:
    """Configuration options for template rendering."""

    template_dir: str | Path | None = None
    base_url: str | None = None
    strict_variables: bool = False


class TemplateRenderer(ABC):
    """Abstract base class for template rendering engines."""

    @abstractmethod
    def render(
        self,
        template_name: str,
        data: TemplateData,
        options: TemplateRenderOptions | None = None,
    ) -> str:
        """Render a template and return the generated HTML."""
        ...