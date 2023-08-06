from click import Command as ClickCommand

from rapidexec.commands.command import BaseCommand


class RapidExecClickCommand(ClickCommand):
    def __init__(self, name, **kwargs):
        self.ignore_unknown_options = True
        self.allow_extra_args = True
        self.rapidexec_command: BaseCommand = kwargs.pop("rapidexec_command", None)
        super().__init__(name, **kwargs)

        for option in self.rapidexec_command.get_click_options():
            self.params.append(option)

    def invoke(self, ctx):
        super().invoke(ctx)
        rapidexec_command = getattr(self, "rapidexec_command")
        rapidexec_command(**ctx.params).execute()
