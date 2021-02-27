import click

@click.command()
@click.option(
    '--action',
    prompt="Please select an action: 1 - create a user, "
           "2 - login, "
           "3 - update password, "
           "4 - delete user account"
)

def main(action):
    click.echo('Hello %s!' % action)

if __name__ == '__main__':
    main()