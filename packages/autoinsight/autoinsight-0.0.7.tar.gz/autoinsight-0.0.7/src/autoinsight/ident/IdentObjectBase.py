from abc import abstractmethod
from uuid import UUID

from autoinsight.common.ObjectBase import ObjectBase
from autoinsight.common.Utils import GUID


class IdentObjectBase(ObjectBase):
    def __init__(self, *args, **kwargs):
        self._id = GUID()
        self._repr = None
        self._str = None
        self._automationInstance = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def description(self) -> str:
        """
        A description that will unique locate the object within the context
        """
        pass

    @property
    def classname(self):
        """
        The control class name
        """
        return type(self).__name__

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def snapshot(self):
        pass
