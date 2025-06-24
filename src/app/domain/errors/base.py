from dataclasses import dataclass
from gettext import gettext


@dataclass()
class BaseDomainError(Exception):
    """Base class for domain errors."""

    detail: str


@dataclass()
class ValidationError(BaseDomainError):
    """Validation error class."""

    detail: str = gettext("Validation error")
