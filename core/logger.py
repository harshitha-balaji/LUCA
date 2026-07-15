"""
Application event logger.

This module provides a lightweight logging system used throughout
the robotic arm controller. It stores application events and allows
the user interface to retrieve them for display in the Event Log.

Responsibilities:
- Record application events
- Categorize events by severity
- Store event history
- Provide access to logged events

This module does not:
- Write log files
- Print to the console
- Depend on the user interface
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from threading import Lock


class LogLevel(Enum):
    """
    Severity level for application events.
    """

    SYSTEM = "SYSTEM"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(slots=True)
class LogEvent:
    """
    Represents a single application event.
    """

    timestamp: datetime
    level: LogLevel
    message: str


class Logger:
    """
    Stores application events.

    The logger maintains an in-memory history of events that can
    later be displayed by the graphical user interface.
    """

    def __init__(self) -> None:
        self._events: list[LogEvent] = []
        self._lock = Lock()

    def log(
        self,
        level: LogLevel,
        message: str,
    ) -> None:
        """
        Record a new application event.

        Args:
            level:
                Severity of the event.

            message:
                Event description.
        """

        event = LogEvent(
            timestamp=datetime.now(),
            level=level,
            message=message,
        )

        with self._lock:
            self._events.append(event)

    def info(self, message: str) -> None:
        """Record an informational event."""

        self.log(LogLevel.INFO, message)

    def success(self, message: str) -> None:
        """Record a successful operation."""

        self.log(LogLevel.SUCCESS, message)

    def warning(self, message: str) -> None:
        """Record a warning."""

        self.log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        """Record an error."""

        self.log(LogLevel.ERROR, message)

    def system(self, message: str) -> None:
        """Record a system event."""

        self.log(LogLevel.SYSTEM, message)

    def get_events(self) -> list[LogEvent]:
        """
        Return all recorded events.
        """

        with self._lock:
            return self._events.copy()

    def clear(self) -> None:
        """
        Remove all recorded events.
        """

        with self._lock:
            self._events.clear()