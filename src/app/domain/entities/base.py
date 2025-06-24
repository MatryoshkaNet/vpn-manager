from dataclasses import dataclass, field

from app.domain.events.base import BaseEvent
from app.domain.value_objects.base import EntityId


@dataclass(kw_only=True)
class BaseEntity:
    """
    Base class for domain entities.

    Manages the entity identifier and collects domain events.
    """

    id: EntityId
    _events: list[BaseEvent] = field(default_factory=list)

    def record_event(self, event: BaseEvent) -> None:
        """Append event to pull events for this entity."""
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        """
        Retrieve and clear recorded domain events for this entity.

        :return: List of BaseEvent instances that were recorded.
        """
        events, self._events = self._events, []
        return events
