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
    m3ufiles_min1 = m3ufiles[-1]
    nf.list_playlists()
    pls = nf.get_playlists()
    pls_min1 = pls[-1]

    print(f"{m3ufiles_min1}")
    print(f"{m3ufiles_min1.parent}")
    print(f"{m3ufiles_min1.name}")
    print(f"{pls_min1}")


if __name__ == '__main__':
    m3utonumber()
