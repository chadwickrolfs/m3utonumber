import click
from numberfiles import NumberFiles


@click.command()
@click.argument('src', type=click.Path(exists=True), nargs=1)
def m3utonumber(src):
    nf = NumberFiles(src)
    m3ufiles = nf.get_m3ufiles()
    print(f"{m3ufiles}")


if __name__ == '__main__':
    m3utonumber()
