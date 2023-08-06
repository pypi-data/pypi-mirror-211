from os import path
import toml
from click import Option, Path
from typing import List, Dict, Union
from dataclasses import dataclass

from rich import box
from rich.console import Console
from rich.table import Table

from rapidexec.commands.command import BaseCommand
from rapidexec.commands.filters import IncludeExcludeFilter, Filter


@dataclass
class ReadTomlCommand(BaseCommand):
    """
    Command for reading and parsing pyproject.toml file
    """

    console: Console = Console()
    table: Table = Table(
        show_header=True,
        box=box.HEAVY_HEAD,
        header_style="bold",
        safe_box=True,
    )

    def __init__(self, **kwargs):
        filters = self.generate_filters(**kwargs)
        super().__init__(filters=filters, **kwargs)

    def validate_include_exclude(self) -> None:
        """
        Validate that a dependency group is not in both include and exclude.
        """
        include_groups = self.kwargs.get("include", [])
        exclude_groups = self.kwargs.get("exclude", [])
        intersect = set(include_groups) & set(exclude_groups)
        if intersect:
            raise ValueError(
                f"Dependency group(s) {intersect} cannot be both included and excluded."
            )

    def generate_filters(self, **kwargs) -> List[Filter]:
        include = kwargs.get("include", [])
        exclude = kwargs.get("exclude", [])
        return [IncludeExcludeFilter(include=include, exclude=exclude)]

    @classmethod
    def get_click_options(cls) -> List[Option]:
        return [
            Option(
                ["--include", "-i"], multiple=True, help="Dependency groups to include."
            ),
            Option(
                ["--exclude", "-e"], multiple=True, help="Dependency groups to exclude."
            ),
            Option(
                ["--file", "-f"],
                default="pyproject.toml",
                help="Path to the pyproject.toml file.",
                type=Path(),
            ),
            Option(
                ["--output", "-o"],
                default="requirements.txt",
                help="Path to the output file.",
                type=Path(),
            ),
        ]

    def get_data(self, **kwargs) -> Dict[str, List[str]]:
        file = kwargs.get("file", "pyproject.toml")
        with open(file, "r") as f:
            try:
                data = toml.load(f)
            except toml.TomlDecodeError as e:
                raise ValueError(f"Error parsing {file}: {e}")

        required_dependencies = data.get("project", {}).get("dependencies", [])
        optional_dependencies = data.get("project", {}).get("optional-dependencies", {})

        if not required_dependencies and not optional_dependencies:
            raise KeyError(
                "No 'dependencies' or 'optional-dependencies' found in the project data."
            )

        dependencies = {
            "required": required_dependencies,
            "optional": optional_dependencies,
        }

        return dependencies

    def apply_filters(self, data) -> Union[List[str], Dict[str, Dict[str, List[str]]]]:
        filtered_data = {}
        for key, value in data.items():
            if key == "required":
                filtered_data[key] = value
            else:
                for f in self.filters:
                    value = f.apply(value)
                filtered_data[key] = value
        return filtered_data

    def create_table(self, data):
        self.table.add_column("REQUIRED Dependencies")
        for optional_key in data.get("optional", {}):
            self.table.add_column(f"{optional_key.upper()} Dependencies")
        max_rows = len(data.get("required", []))
        if data.get("optional", {}):
            for optional_key in data.get("optional", {}):
                if len(data["optional"][optional_key]) > max_rows:
                    max_rows = len(data["optional"][optional_key])

        for i in range(max_rows):
            row = [data["required"][i] if i < len(data["required"]) else ""]
            for optional_key in data.get("optional", {}):
                row.append(
                    data["optional"][optional_key][i]
                    if i < len(data["optional"][optional_key])
                    else ""
                )
            self.table.add_row(*row, style="green")

    def execute(self) -> None:
        try:
            self.validate_include_exclude()
            data = self.get_data(**self.kwargs)
            output_file = self.kwargs.get("output", "requirements.txt")
            output_path = path.abspath(output_file)
            if not path.isdir(path.dirname(output_path)):
                raise ValueError(
                    f"Output directory does not exist: {path.dirname(output_path)}"
                )
            filtered_data = self.apply_filters(data)
            self.create_table(filtered_data)
            with open(output_path, "w") as f:
                for key, value in filtered_data.items():
                    if isinstance(value, list) and key == "required":
                        for v in value:
                            f.write(f"{v}\n")
                    elif isinstance(value, dict):
                        for group, deps in value.items():
                            f.write(f"\n# {group}\n")
                            for dep in deps:
                                f.write(f"{dep}\n")
                    else:
                        raise ValueError(f"Unexpected format for {key}")
            self.console.print(self.table)
            self.console.print(f"Requirements written to {output_path}")
        except Exception as e:
            self.table.add_column(
                "Exception Type", width=20, style="cyan", header_style="bold"
            )
            self.table.add_column(
                "Exception Message", width=80, style="red", header_style="bold"
            )
            self.table.add_row(e.__class__.__name__, str(e))
            self.console.print(self.table)
