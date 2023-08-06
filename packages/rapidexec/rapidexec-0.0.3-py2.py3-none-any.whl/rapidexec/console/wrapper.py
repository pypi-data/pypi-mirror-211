import random
import time

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from rapidexec.console.singleton import LiveDisplaySingleton


def simulate_installation(
    progress,
    overall_progress,
    task_id,
    overall_task_id,
    weight,
    min_seconds=2,
    max_seconds=5,
):
    """Simulate an installation process by incrementally updating a task."""
    for _ in range(100):
        time.sleep(random.uniform(min_seconds, max_seconds) / 100)
        progress.update(task_id, advance=1)
        overall_progress.update(overall_task_id, advance=weight)


class ConsoleWrapper(Console):
    console = Console()
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live = LiveDisplaySingleton.go_online(
            self,
        )

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def print_exception(self, *args, **kwargs):
        try:
            self.console.print_exception(*args, **kwargs)
        except Exception as err:
            self.print(err)
