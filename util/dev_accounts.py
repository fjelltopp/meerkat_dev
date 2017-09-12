"""
This is a utility script to help store the developer's personal details in the
correct manner so that local databases can be setup with the developer's
account and messaging details.

Run:
    `account_details.py --list` (To view existing accounts)
    `account_details.py --clear` (To clear all accounts)
    `account_details.py --add` (To add a new account)
    `account_details.py --remove username` (To remove an account)

If no flag is provided it will list the existing accounts.

For changes to have an effect in the dev envirnoment, this script must be run
before starting the dev environment, or if the the dev environment is already
up, then the command `local_db.py` must be rerun in the auth and hermes docker
containers.
"""
import pip
import ast
import os
from getpass import getpass

# For the password hashing - passlib may or may not already be installed.
try:
    from passlib.hash import pbkdf2_sha256
except ImportError:
    pip.main(['install', 'passlib'])
    from passlib.hash import pbkdf2_sha256


# A utility function to require input when necessary.
def required_input(string):
    value = raw_input(string)
    while not value:
        print("Value required, try again.")
        value = raw_input(string)
    return value


# The file name of the file that will store account details.
FILENAME = (os.path.dirname(os.path.realpath(__file__)) +
            '/../.settings/accounts.cfg')


def users(args, extra):

    # Read the existing users file as a dictionary.
    try:
        users_file = open(FILENAME, 'r+').read()
        users = ast.literal_eval(users_file)
    except IOError:
        users = {}
    except SyntaxError:
        users = {}
    print('')

    # PERFORM THE DESIRED ACTION
    # List the accounts already created.
    if args.list:

        # Set things up
        if users:
            print("Here are the accounts currently added by the developer:")
        else:
            print("No accounts created by the developer yet.")

        for username, user in users.items():
            print("{} {} ({}) - {} {}".format(
                user['first_name'],
                user['last_name'],
                user['username'],
                user['email'],
                user['sms']
            ))

    # Add a new developer account.
    if args.add:

        # Set things up
        user = {}
        print("Adding a developer's account...")
        print("Please give the following information:")

        # Get account information from user.
        user['username'] = required_input('Username*: ')
        user['first_name'] = required_input('First Name*: ')
        user['last_name'] = raw_input('Last Name: ')
        user['email'] = required_input('Email*: ')
        user['sms'] = raw_input('SMS number: ')
        user['slack'] = '@' + raw_input('Meerkat Slack Username: ')
        print('Passwords will be hashed.')
        password = getpass('Password*: ')
        password2 = getpass('Retype password*: ')
        while password != password2:
            print("Passwords must match.  Please try again.")
            password = getpass('Password*: ')
            password2 = getpass('Retype password*: ')
        user['password'] = pbkdf2_sha256.encrypt(password)

        # Store account information.
        users[user['username']] = user

        print('\n\nUser Added:')
        print("{} {} ({}) - {} {} {}".format(
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['sms'],
            user['slack']
        ))

    # Remove an already existing account.
    if args.remove:

        # Set things up
        print("Removing a developer's account:")
        username = required_input('Username*: ')
        while username not in users.keys():
            print('User doesn\'t exist. Try again.')
            username = required_input('Username*: ')

        # Check that the user really wants to delete the user.
        check_str = 'Are you sure you want to remove {}? y/n '.format(username)
        check = raw_input(check_str)
        while check != ('y' or 'n'):
            print('Must respond with \'y\' or \'n\'.')
            check = raw_input(check_str)

        # Perform the action
        if check is 'y':
            del users[username]
            print("User Deleted")
        else:
            print("Cancelled deletion. User remains.")

    # Clear all accounts that have been created.
    if args.clear:

        # Check that the user really wants to clear all accounts.
        check = raw_input('Are you sure you want to clear all accounts? y/n ')
        while check not in ['y', 'n']:
            print('Must respond with \'y\' or \'n\'.')
            check = raw_input('Are you sure you want to clear all accounts? y/n ')

        # Do the clearning.
        if check is 'y':
            users = {}
            print("Accounts cleared")
        else:
            print("Account clearing cancelled. Accounts remain.")

    # Write any changes to file only if we have anything to write.
    if users:
        users_file = open(FILENAME, 'w+')
        users_file.write(str(users))
    print('')
