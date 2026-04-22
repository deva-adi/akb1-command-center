"""AKB1 Command Center backend.

Single source of truth for the application version string. ``app.config``
reads ``__version__`` from this module and every downstream consumer
(``/health``, logs, future API metadata) flows through the settings object.
The M8 release commit drops the ``-dev`` suffix; no other file should
carry a hardcoded version number.
"""

__version__ = "5.7.0-dev"
