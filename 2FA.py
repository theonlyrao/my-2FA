import click
import sys
import crypt
import os


# Common
def user_exists(username):
    exists = False
    with open('/etc/shadow', 'r') as fp:
        for line in fp:
            temp = line.split(':')
            if temp[0] == username:
                exists = True
    return exists


# Login
def update_etc_shadow(username, password, salt, initial_token):
    hashed = crypt.crypt(password + initial_token, '$6$' + salt)
    line = username + ':' + hashed + ":17710:0:99999:7:::"
    file = open("/etc/shadow", "a+")
    file.write(line + '\n')
    file.close()


def create_home_dir(username):
    # noinspection PyBroadException
    try:
        os.mkdir("/home/" + username)
    except Exception:
        click.echo("Directory: /home/" + username + " already exists", err=True)


def update_etc_passwd(username):
    count = 1000
    with open('/etc/passwd', 'r') as f:  # Opening passwd file in read mode
        arr1 = []
        for line in f:
            temp1 = line.split(':')
            while count <= int(temp1[3]) < 65534:  # checking number of existing UID
                count = int(temp1[3]) + 1  # assigning new uid = 1000+number of UIDs +1

    file = open("/etc/passwd", "a+")
    count = str(count)
    entry = username + ':x:' + count + ':' + count + ':,,,:/home/' + username + ':/bin/bash'
    file.write(entry + '\n')
    file.close()


@click.command()
@click.option(
    '--username',
    prompt="Please enter the username for this new user")
@click.option(
    '--password',
    prompt="Please enter the password for this new user")
@click.option(
    '--salt',
    prompt="Please enter the salt for this new user")
@click.option(
    '--initial_token',
    prompt="Please enter the initial token for this new user")
def create_user(username, password, salt, initial_token):
    if user_exists(username):
        click.echo("FAILURE: user %s exists" % username, err=True)
        sys.exit()

    update_etc_shadow(username, password, salt, initial_token)
    create_home_dir(username)
    update_etc_passwd(username)
    click.echo("SUCCESS: %s created" % username)


# Login
def perform_authentication(username, password, current_token, next_token):
    with open('/etc/shadow', 'r') as fp:
        for line in fp:
            temp = line.split(':')
            if temp[0] == username:  # checking whether entered username exist or not
                salt_and_pass = (temp[1].split('$'))  # retrieving salt against the user
                salt = salt_and_pass[2]
                result = crypt.crypt(password + current_token,
                                     '$6$' + salt)  # calculating hash via salt and password entered by user
                if result == temp[1]:  # comparing generated salt with existing salt entery
                    click.echo("SUCCESS: Login Successful")
                    return
                else:
                    click.echo("FAILURE: either passwd or token incorrect", err=True)
                    sys.exit()
    click.echo("FAILURE: user %s does not exist" % username, err=True)
    sys.exit()


@click.command()
@click.option(
    '--username',
    prompt="Please enter your username",
)
@click.option(
    '--password',
    prompt="Please enter your password")
@click.option(
    '--current_token',
    prompt="Please enter your current token")
@click.option(
    '--next_token',
    prompt="Please enter the next token")
def login_user(username, password, current_token, next_token):
    if not user_exists(username):
        click.echo("FAILURE: user %s does not exist" % username, err=True)
        sys.exit()

    perform_authentication(username, password, current_token, next_token)


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
        if int(action) == 1:
            create_user()
        if int(action) == 2:
            login_user()
        else:
            click.echo("Not implemented.", err=True)
    except Exception:
        click.echo("Got an exception: %s" % Exception, err=True)


if __name__ == '__main__':
    main()
