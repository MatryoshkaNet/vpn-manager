import datetime

from dataclasses import dataclass
from typing import Self

from app.utils.datetime import get_server_now


@dataclass(frozen=True, kw_only=True)
class EventPayload:
    """Base class for event payloads."""


@dataclass(frozen=True, kw_only=True)
class EventMetadata:
    """
    Technical metadata for events.

    :param name: Name/type of the event.
    :param occurred_at: UTC timestamp when the event occurred.
    """

    name: str
    occurred_at: datetime.datetime


@dataclass(frozen=True, kw_only=True)
class BaseEvent:
    """
    Base class for domain events.

    :param payload: EventPayload containing domain-specific data.
    :param metadata: EventMetadata with creation details.
    """

    payload: EventPayload
    metadata: EventMetadata

    @classmethod
    def create(cls, payload: EventPayload) -> Self:
        """
        Create an event instance with metadata.

        :param payload: EventPayload containing domain-specific data.
        :return: Instance of the event with populated metadata.
        """
        metadata = EventMetadata(name=f"{cls.__name__}", occurred_at=get_server_now())
        return cls(payload=payload, metadata=metadata)
