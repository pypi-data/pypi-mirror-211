import subprocess
import json

from click import Option

from rapidexec.commands.command import BaseCommand
from rapidexec.commands.filters import ExcludeFilter


class DockerComposeCommand(BaseCommand):
    """
    Command for Docker "ps" operation
    """

    def __init__(self, **kwargs):
        headers = [
            ("ID", "CONTAINER ID"),
            ("Image", "IMAGE"),
            ("Names", "NAMES"),
            ("Command", "COMMAND"),
            ("Ports", "PORTS"),
            ("CreatedAt", "CREATED"),
            ("Status", "STATUS"),
        ]
        filters = self.generate_filters(**kwargs)
        super().__init__(headers, filters, **kwargs)

    def generate_filters(self, **kwargs):
        exclude = kwargs.get("exclude", None)
        return [ExcludeFilter(exclude if exclude else [])]

    @classmethod
    def get_click_options(cls):
        return [
            Option(["--exclude", "-e"], multiple=True, help="Columns to exclude"),
        ]

    def get_data(self, *args, **kwargs):
        output = subprocess.run(
            ["docker-compose", "ps", "--format", "json"], capture_output=True, text=True
        ).stdout
        return [json.loads(line) for line in output.splitlines()]
