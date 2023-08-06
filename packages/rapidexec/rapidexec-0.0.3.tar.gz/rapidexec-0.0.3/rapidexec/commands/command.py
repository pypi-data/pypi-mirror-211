from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Dict, Iterable

from click import Option
from rich.console import Console
from rich.table import Table

from rapidexec.commands.filters import Filter


@dataclass
class Command(metaclass=ABCMeta):
    def __new__(cls, *args, **kwargs):
        if cls == Command or cls.__bases__[0] == Command:
            raise TypeError("Command is an abstract class and cannot be instantiated")
        return super().__new__(cls)

    @abstractmethod
    def execute(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_click_options(cls) -> Iterable[Option]:
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def generate_filters(self, *args, **kwargs):
        pass

    @abstractmethod
    def apply_filters(self, data):
        pass


@dataclass
class BaseCommand(Command):
    """
    Base class for all commands
    """

    def __init__(self, headers=None, filters=None, **kwargs):
        if filters is None:
            filters = []
        if headers is None:
            headers = []
        self.headers = headers
        self.filters = filters
        self.kwargs = kwargs

    @classmethod
    def get_click_options(cls) -> Iterable[Option]:
        raise NotImplementedError

    def get_data(self, *args, **kwargs) -> List:
        raise NotImplementedError

    def generate_filters(self, *args, **kwargs) -> List[Filter]:
        raise NotImplementedError

    def apply_filters(self, data) -> List[Dict[str, str]]:
        for f in self.filters:
            data = f.apply(data)

        # Update self.headers to reflect the keys present in the filtered data
        if data:
            self.headers = [
                (header, title)
                for header, title in self.headers
                if header in data[0].keys()
            ]

        return data

    def create_table(self, filtered_data: List[Dict[str, str]]):
        """
        Create a table with the filtered data
        """
        table = Table(
            show_header=True, header_style="bold magenta", border_style="green"
        )

        for header, display_name in self.headers:
            table.add_column(display_name, style="dim", justify="left")

        for row_data in filtered_data:
            row = [row_data.get(header, "") for header, _ in self.headers]
            table.add_row(*row)

        return table

    def execute(self) -> None:
        raw_data = self.get_data(**self.kwargs)
        if not raw_data:
            return
        filtered_data = self.apply_filters(raw_data)
        table = self.create_table(filtered_data)

        console = Console()
        console.print(table)
