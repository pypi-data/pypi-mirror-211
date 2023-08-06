# progress_manager.py
import asyncio

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn


class ProgressManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_progress()
        return cls._instance

    def init_progress(self):
        self.progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.tasks = {}

    def add_task(self, description, total=100):
        try:
            task_id = self.progress.add_task(description, total=total)
            self.tasks[description] = task_id
        except ValueError as err:
            raise Exception(f"Choices: {self.tasks.keys()}", err)
        return task_id

    def update_task(self, description, advance=1):
        try:
            task_id = self.tasks[description]
        except KeyError as err:
            raise Exception(f"Choices: {self.tasks.keys()}", err)
        self.progress.update(task_id, advance=advance)
        if self.progress.tasks[task_id].completed >= self.progress.tasks[task_id].total:
            self.progress.stop_task(task_id)
