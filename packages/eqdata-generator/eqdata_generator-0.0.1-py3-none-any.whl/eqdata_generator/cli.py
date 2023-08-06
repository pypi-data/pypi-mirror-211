import click

@click.command()
@click.option('--count',default=1,help='number of greetings.')
@click.option('--name',prompt='your name', help='the person to greet')
def cli(count,name):
    for x in range(count):
        click.echo(f"hello {name}")