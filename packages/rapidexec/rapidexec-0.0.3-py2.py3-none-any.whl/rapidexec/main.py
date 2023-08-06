import click
from rapidexec.cli import RapidExecCLI


@click.command(cls=RapidExecCLI, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


if __name__ == "__main__":
    # Accept all options
    cli()
