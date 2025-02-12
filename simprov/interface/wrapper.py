from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simprov.core import SimProv


class BlueprintWrapper(ABC):

    def __init__(self, simprov: 'SimProv') -> None:
        self.simprov: 'SimProv' = simprov
        self.blueprint = self._build_blueprint()
        super().__init__()

    @abstractmethod
    def _build_blueprint(self):
        pass
