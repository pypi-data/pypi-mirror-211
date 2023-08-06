import docker

from rich.live import Live
from rich.prompt import Prompt
from click import Option
from rich.table import Table

from rapidexec.commands.command import BaseCommand


class DockerLogsCommand(BaseCommand):
    """
    Command for Docker logs retrieval
    """

    def __init__(self, **kwargs):
        headers = [
            ("Log", "LOG"),
            ("Stream", "STREAM"),
            ("Time", "TIME"),
        ]
        super().__init__(headers, [], **kwargs)

    @classmethod
    def get_click_options(cls):
        return [
            Option(["--container"], help="Container name or image ID"),
        ]

    def get_data(self, *args, **kwargs):
        container = kwargs.get("container", None)
        if not container:
            container = Prompt.ask("Enter container name or image ID")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Log")
        table.add_column("Stream")
        table.add_column("Time")
        client = docker.from_env()
        container = client.containers.get(container)
        with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
            for line in container.logs(stream=True):
                print(line.decode("utf-8").strip())

    def execute(self) -> None:
        self.get_data(**self.kwargs)
