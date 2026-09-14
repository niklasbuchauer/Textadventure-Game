"""Small, synchronous event bus for gameplay-to-presentation communication.

Gameplay code emits facts (damage, rewards, intent) and never reaches into a
Pygame widget.  Presentation code subscribes to those facts.  The bus is
intentionally dependency-free so combat simulations and tests can use it too.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, DefaultDict


@dataclass(frozen=True)
class GameEvent:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)


EventListener = Callable[[GameEvent], None]


class EventManager:
    """A deterministic in-process event dispatcher.

    ``emit`` is synchronous by design: UI state is current before the next
    frame, and tests can assert outcomes without running a game loop.
    """

    def __init__(self) -> None:
        self._listeners: DefaultDict[str, list[EventListener]] = defaultdict(list)

    def subscribe(self, name: str, listener: EventListener) -> Callable[[], None]:
        self._listeners[name].append(listener)

        def unsubscribe() -> None:
            try:
                self._listeners[name].remove(listener)
            except ValueError:
                pass

        return unsubscribe

    def emit(self, name: str, **payload: Any) -> GameEvent:
        event = GameEvent(name=name, payload=payload)
        for listener in tuple(self._listeners.get(name, ())):
            listener(event)
        return event
