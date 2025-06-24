import uuid

from dataclasses import dataclass, field

from app.domain.errors.base import ValidationError


@dataclass(frozen=True)
class BaseValueObject[ValueT]:
    """
    Base class for value objects.

    Provides immutability, automatic validation, and conversion to primitive value.
    """

    _value: ValueT

    def __post_init__(self) -> None:
        """Validate the value after initialization."""
        self.validate()

    def to_python(self) -> ValueT:
        """
        Return the underlying primitive Python value.

        :return: The wrapped primitive value.
        """
        return self._value

    def validate(self) -> None:
        """
        Enforce custom validation logic defined in subclasses.

        :raises NotImplementedError: If not overridden in subclass.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.validate() must be implemented")

    def __repr__(self) -> str:
        """Return the developer-friendly representation of the value object."""
        return f"{self.__class__.__name__}({self._value!r})"

    def __str__(self) -> str:
        """
        Return the string representation of the underlying value.

        :return: String form of the value.
        """
        return str(self._value)


@dataclass(frozen=True)
class EntityId(BaseValueObject[uuid.UUID]):
    """
    Value object for entity identifiers.

    Wraps UUID version 7.
    """

    _value: uuid.UUID = field()

    def validate(self) -> None:
        """
        Ensure the UUID conforms to version 7.

        :raises ValidationError: If the underlying UUID version is not 7.
        """
        assert self._value.version == 7, ValidationError("Invalid version uuid")
