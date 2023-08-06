"""
Django's support for templates.

The paradoxdjango.template namespace contains two independent subsystems:

1. Multiple Template Engines: support for pluggable template backends,
   built-in backends and backend-independent APIs
2. Django Template Language: Django's own template engine, including its
   built-in loaders, context processors, tags and filters.

Ideally these subsystems would be implemented in distinct packages. However
keeping them together made the implementation of Multiple Template Engines
less disruptive .

Here's a breakdown of which modules belong to which subsystem.

Multiple Template Engines:

- paradoxdjango.template.backends.*
- paradoxdjango.template.loader
- paradoxdjango.template.response

Django Template Language:

- paradoxdjango.template.base
- paradoxdjango.template.context
- paradoxdjango.template.context_processors
- paradoxdjango.template.loaders.*
- paradoxdjango.template.debug
- paradoxdjango.template.defaultfilters
- paradoxdjango.template.defaulttags
- paradoxdjango.template.engine
- paradoxdjango.template.loader_tags
- paradoxdjango.template.smartif

Shared:

- paradoxdjango.template.utils

"""

# Multiple Template Engines

from .engine import Engine
from .utils import EngineHandler

engines = EngineHandler()

__all__ = ("Engine", "engines")


# Django Template Language

# Public exceptions
from .base import VariableDoesNotExist  # NOQA isort:skip
from .context import Context, ContextPopException, RequestContext  # NOQA isort:skip
from .exceptions import TemplateDoesNotExist, TemplateSyntaxError  # NOQA isort:skip

# Template parts
from .base import (  # NOQA isort:skip
    Node,
    NodeList,
    Origin,
    Template,
    Variable,
)

# Library management
from .library import Library  # NOQA isort:skip

# Import the .autoreload module to trigger the registrations of signals.
from . import autoreload  # NOQA isort:skip


__all__ += ("Template", "Context", "RequestContext")
