import asyncio
import random
from rapidexec.console.progress_manager import ProgressManager


async def main(*args, **kwargs):
    progress_manager = ProgressManager()
    task_id = progress_manager.add_task("[cyan]File3 task", total=100)

    for _ in range(100):
        await asyncio.sleep(random.random() / 10)
        progress_manager.update_task("[cyan]File3 task", advance=1)
