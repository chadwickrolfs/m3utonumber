import click
from numberfiles import NumberFiles


@click.command()
@click.argument('src', type=click.Path(exists=True), nargs=1)
def m3utonumber(src):
    nf = NumberFiles(src)
    nf.numberfiles()


if __name__ == '__main__':
    m3utonumber()
