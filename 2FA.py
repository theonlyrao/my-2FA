import click


# Login
def login():
    pass


@click.command()
@click.option(
    '--action',
    prompt="Please select an action: 1 - create a user, "
           "2 - login, "
           "3 - update password, "
           "4 - delete user account"
)
def main(action):
    # noinspection PyBroadException
    try:
        click.echo('Hello %s!' % action)
        if int(action) == 1:
            login()
        else:
            click.echo("Not implemented.", err=True)
    except Exception:
        click.echo("Got an exception: %s" % Exception, err=True)


if __name__ == '__main__':
    main()
