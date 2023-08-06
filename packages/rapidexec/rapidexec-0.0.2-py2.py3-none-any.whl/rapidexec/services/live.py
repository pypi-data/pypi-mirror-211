import time
from typing import Iterable

from click import Option
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    Progress,
    TimeElapsedColumn,
    BarColumn,
    TextColumn,
    SpinnerColumn,
)

from rapidexec.commands.command import BaseCommand


current_app_progress = Progress(TimeElapsedColumn(), TextColumn("{task.description}"))
step_progress = Progress(
    TextColumn("  "),
    TimeElapsedColumn(),
    TextColumn("[bold purple]{task.fields[action]}"),
    SpinnerColumn("simpleDots"),
)
app_steps_progress = Progress(
    TextColumn(
        "[bold blue]Progress for app {task.fields[name]}: {task.percentage:.0f}%"
    ),
    BarColumn(),
    TextColumn("({task.completed} of {task.total} steps done)"),
)
overall_progress = Progress(
    TimeElapsedColumn(), BarColumn(), TextColumn("{task.description}")
)

progress_group = Group(
    Panel(Group(current_app_progress, step_progress, app_steps_progress)),
    overall_progress,
)

step_actions = ("downloading", "configuring", "building", "installing")
tasks = [("Task1", (2, 1, 4, 2)), ("Task2", (1, 3, 8, 4))]

overall_task_id = overall_progress.add_task("", total=len(tasks))


def run_steps(name, step_times, app_steps_task_id):
    for idx, step_time in enumerate(step_times):
        action = step_actions[idx]
        step_task_id = step_progress.add_task("", action=action, name=name)

        for _ in range(step_time):
            time.sleep(0.5)
            step_progress.update(step_task_id, advance=1)

        step_progress.stop_task(step_task_id)
        step_progress.update(step_task_id, visible=False)

        app_steps_progress.update(app_steps_task_id, advance=1)


class LiveCommand(BaseCommand):
    """
    Test command for live output
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

    @classmethod
    def get_click_options(cls) -> Iterable[Option]:
        return []

    def generate_filters(self, **kwargs):
        return []

    def execute(self) -> None:
        with Live(progress_group):
            for idx, (name, step_times) in enumerate(tasks):
                top_descr = "[bold #AAAAAA](%d out of %d tasks completed)" % (
                    idx,
                    len(tasks),
                )
                overall_progress.update(overall_task_id, description=top_descr)

                current_task_id = current_app_progress.add_task("Executing %s" % name)
                app_steps_task_id = app_steps_progress.add_task(
                    "", total=len(step_times), name=name
                )
                run_steps(name, step_times, app_steps_task_id)

                app_steps_progress.update(app_steps_task_id, visible=False)
                current_app_progress.stop_task(current_task_id)
                current_app_progress.update(
                    current_task_id, description="[bold green]%s completed!" % name
                )

                overall_progress.update(overall_task_id, advance=1)

            overall_progress.update(
                overall_task_id,
                description="[bold green]%s tasks completed, done!" % len(tasks),
            )
