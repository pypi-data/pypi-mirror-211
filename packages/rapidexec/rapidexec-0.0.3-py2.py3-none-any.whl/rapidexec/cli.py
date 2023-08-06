import importlib
from typing import Optional

import click
import os

from rapidexec.commands.base import RapidExecClickCommand
from rapidexec.commands.command import BaseCommand

plugin_folder = os.path.join(os.path.dirname(__file__), "services")


class RapidExecCLI(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rapidexec_click_command: Optional[RapidExecClickCommand] = None

    def list_commands(self, ctx):
        rv = []
        for root, dirs, files in os.walk("rapidexec/services"):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    command_name = os.path.join(root, filename)[
                        len("rapidexec/services/") : -len(".py")
                    ].replace("/", "-")
                    rv.append(command_name)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            module_path = "rapidexec.services." + name.replace("-", ".")
            module = importlib.import_module(module_path)
        except ImportError as e:
            print(e)
            return

        for attr_name in dir(module):
            attr_value = getattr(module, attr_name)
            if (
                isinstance(attr_value, type)
                and issubclass(attr_value, BaseCommand)
                and attr_value is not BaseCommand
            ):
                self.rapidexec_click_command = RapidExecClickCommand(
                    name, rapidexec_command=attr_value
                )
                return self.rapidexec_click_command
