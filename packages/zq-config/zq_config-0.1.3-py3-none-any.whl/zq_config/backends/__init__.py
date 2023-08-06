import abc
import sys
from types import ModuleType
from typing import Dict, Optional, Tuple



class Backend:
    @abc.abstractmethod
    def get(self, data_id, data_group) -> Optional[str]:
        raise NotImplementedError
