from abc import ABC, abstractmethod

from cartesio.core.helper import Observer


class Callback(Observer, ABC):
    def __init__(self, frequency=1):
        self.frequency = frequency
        self.decoder = None

    def set_decoder(self, decoder):
        self.decoder = decoder

    def update(self, event):
        if event["n"] % self.frequency == 0 or event["force"]:
            self._callback(event["n"], event["name"], event["content"])

    @abstractmethod
    def _callback(self, n, e_name, e_content):
        pass
