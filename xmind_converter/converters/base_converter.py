"""Base converter abstract class"""

from abc import ABC, abstractmethod
from ..models import MindMap


class BaseConverter(ABC):
    """Base converter abstract class"""

    @abstractmethod
    def convert_to(self, mindmap: MindMap, output_path: str, **kwargs) -> None:
        """Convert MindMap to file

        Args:
            mindmap: MindMap object to convert
            output_path: Path to save the output file
            **kwargs: Additional format-specific parameters
        """
        pass
