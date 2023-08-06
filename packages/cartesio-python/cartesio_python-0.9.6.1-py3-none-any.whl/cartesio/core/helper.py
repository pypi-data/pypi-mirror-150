from abc import ABC, abstractmethod
from typing import List


def catalog_decorator(cls):
    cls.fill()
    return cls


class Prototype(ABC):
    """
    Using Prototype Pattern to duplicate:
    https://refactoring.guru/design-patterns/prototype
    """

    @abstractmethod
    def clone(self):
        pass


class Factory(object):
    """
    Using Factory Pattern:
    https://refactoring.guru/design-patterns/factory-method
    """

    def __init__(self, prototype):
        self._prototype = None
        self.set_prototype(prototype)

    def set_prototype(self, prototype):
        self._prototype = prototype

    def create(self):
        return self._prototype.clone()


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, event):
        """
        Receive update from subject.
        """
        pass


class Observable(ABC):
    """
    For the sake of simplicity, the Observable's state, essential to all
    subscribers, is stored in this variable.
    """

    def __init__(self):
        self._observers: List[Observer] = []

    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def clear(self) -> None:
        self._observers = []

    """
    The subscription management methods.
    """

    def notify(self, event) -> None:
        """
        Trigger an update in each subscriber.
        """

        for observer in self._observers:
            observer.update(event)
