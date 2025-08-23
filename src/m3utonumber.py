import click
import pathlib

from numberfiles import NumberFiles


click_path = click.Path(
    exists=True,
    file_okay=False,
    path_type=pathlib.Path,
    executable=True,
)


@click.command()
@click.argument('src', type=click_path, nargs=1)
def m3utonumber(src):
    nf = NumberFiles(src)
    m3ufiles = nf.get_m3ufiles()
    print(f"{m3ufiles}")


if __name__ == '__main__':
    m3utonumber()
