from __future__ import annotations
from typing import List
from azul.interfaces import NotifyEverybodyInterface, ObservableInterface, ObserverInterface


class GameObservable(NotifyEverybodyInterface, ObservableInterface):
    """Keeps list of Observers which are notified upon change in Game"""

    _observers: List[ObserverInterface]

    def __init__(self) -> None:
        self._observers = []

    def register_observer(self, observer: ObserverInterface) -> None:
        """Registers new observer"""
        self._observers.append(observer)

    def cancel_observer(self, observer: ObserverInterface) -> None:
        """If observer was registered, cancels the subscription"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_everybody(self, state: str) -> None:
        """Notifies all observers about change"""
        observer: ObserverInterface
        for observer in self._observers:
            observer.notify(state)

    def get_observers(self) -> List[ObserverInterface]:
        """Returns list of all current observers"""
        return self._observers.copy()
