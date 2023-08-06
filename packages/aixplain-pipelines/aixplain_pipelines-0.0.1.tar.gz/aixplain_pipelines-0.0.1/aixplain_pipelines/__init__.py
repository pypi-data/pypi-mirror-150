"""
aiXplain Pipelines Library.
---

aiXplain Pipelines enables python programmers to add AI functions
to their software.
"""

from .aixplain_pipelines import Pipeline


# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())