import click

from connect4.controllers import Connect4Controller


@click.command()
def main() -> None:
    controller = Connect4Controller()
    try:
        controller.start()
    except KeyboardInterrupt:
        click.echo(click.style("Game stopped by user. Thanks for playing!", fg="green"))


if __name__ == "__main__":  # pragma: no cover
    main()
