"""Base converter abstract class"""

from abc import ABC, abstractmethod
from ..models import MindMap


class BaseConverter(ABC):
    """Base converter abstract class"""

    @abstractmethod
    def convert_to(self, mindmap: MindMap) -> str:
        """Convert MindMap to string format

        Args:
            mindmap: MindMap object to convert

        Returns:
            String representation of the mindmap in the specific format
        """
        pass

    @abstractmethod
    def convert_from(self, input_path: str) -> MindMap:
        """Convert from file format to MindMap

        Args:
            input_path: Path to the input file

        Returns:
            MindMap object created from the file
        """
        pass
