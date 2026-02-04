"""Base parser abstract class"""

from abc import ABC, abstractmethod
from ..models import MindMap


class BaseParser(ABC):
    """Base parser abstract class for parsing files into MindMap"""

    @abstractmethod
    def parse(self, file_path: str) -> MindMap:
        """Parse file and return MindMap object

        Args:
            file_path: Path to the file to parse

        Returns:
            MindMap object created from the file
        """
        pass
