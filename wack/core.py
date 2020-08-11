import click

from wack.importing import import_wack


class WackCommand(click.Command):
    pass


echo = click.echo


def command(*args, **kwargs):
    """copied from click.decorators.command"""
    from click.decorators import command

    def decorator(f):
        # todo allow passing of other Command classes
        kwargs["cls"] = WackCommand
        cmd = command(*args, **kwargs)(f)
        return cmd

    return decorator


class CLI(click.Group):
    """custom base cli for $ wack"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_commands()

    def add_commands(self):
        """add commands from wack.py to cli"""
        try:
            wack = import_wack()
            for name, item in vars(wack).items():
                if isinstance(item, WackCommand):
                    self.add_command(item, name=name)
        except FileNotFoundError:
            pass
