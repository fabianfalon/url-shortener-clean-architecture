import logging
from typing import List, Dict, Type, Callable

from src.domain.events import DomainEvent, EventBus


class InMemoryEventBus(EventBus):
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}
        self._logger = logging.getLogger(__name__)

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Subscribe a handler to a specific event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        self._logger.info(f"Handler subscribed to {event_type.__name__}")

    def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribed handlers"""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event)
                    self._logger.info(
                        f"Event {event_type.__name__} handled successfully"
                    )
                except Exception as e:
                    self._logger.error(
                        f"Error handling event {event_type.__name__}: {str(e)}"
                    )


class AsyncEventBus(EventBus):
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}
        self._logger = logging.getLogger(__name__)

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Subscribe a handler to a specific event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        self._logger.info(f"Handler subscribed to {event_type.__name__}")

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribed handlers asynchronously"""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    await handler(event)
                    self._logger.info(
                        f"Event {event_type.__name__} handled successfully"
                    )
                except Exception as e:
                    self._logger.error(
                        f"Error handling event {event_type.__name__}: {str(e)}"
                    )
