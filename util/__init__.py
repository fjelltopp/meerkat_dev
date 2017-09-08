import repo
import subprocess
import os
from xml.etree import ElementTree
from datetime import datetime

DUMPS_PATH = os.path.abspath(os.path.dirname(__file__)) + "/../abacus/dumps/"
MANIFEST_URL = "git@github.com:meerkat-code/meerkat.git"


def run_repo(args, extra):
    """
    Run's a Google Repo command by just forwarding the supplied args to the
    main() function of the Google Repo script.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    if args.action == "repo":
        print(extra)
        repo.main(extra)
    else:
        repo.main([args.action] + extra)


def dump(args, extra):
    """
    Takes a database dump and stores it in the DB_DUMPS_FOLDER.
    DB dumps are named using the country, date, time and an optional tag
    specified by the user: <country>_<date>_<time>_<tag>.psql.
    """
    if args.list:
        dumps = os.listdir(DUMPS_PATH)
        print("Dumps are currently stored in:\n    " + DUMPS_PATH)
        print("Available dumps:")
        for dump in dumps:
            print("    " + dump)
        return

    # Get params for the filename. The country is stored in DB env variable
    time = datetime.now().strftime("%y%m%d_%H%M%S")
    country = subprocess.check_output([
        "sudo", "docker",  "exec", "-ti", "compose_db_1", "sh", "-c",
        "echo \"$COUNTRY\""
    ]).strip()

    # Set the file name using the tag only if it is available.
    if args.tag:
        filename = DUMPS_PATH + "{}_{}_{}.psql".format(
            country,
            time,
            args.tag
        )
    else:
        filename = DUMPS_PATH + "{}_{}.psql".format(
            country,
            time
        )

    # Get the dump by executing pg_dump in the db container
    # Executing in container ensures same client and server version of pg_dump
    subprocess.check_output([
        "sh", "-c",
        "sudo docker exec -ti compose_db_1 sh -c "
        "\"pg_dump -U postgres -h localhost meerkat_db\" > " + filename
    ])


def setup(args, extra):
    """
    Initialises the parent directory to be the Meerkat code base folder.
    Optionally specify which manifest to use.
    """
    print('Setting up the Meerkat codebase...')
    print('This will destroy changes, resetting everything to the remote.')
    if raw_input('ARE YOU SURE YOU WANT TO CONTINUE? (Y/n) ') is 'Y':
        repo.main(['init', '-u', MANIFEST_URL] + extra)
        repo.main(['sync', '--force-sync'])
        print('Meerkat code synced')
        repo.main(['forall', '-c', 'git', 'checkout', 'master'])
        try:
            repo.main(
                ['forall', '-c', 'git', 'checkout', '-q', 'development']
            )
        except subprocess.CalledProcessError:
            print('Some repos do not have a development branch.')
        print('Master and Development branches created on your '
              'local machine.\nDevelopment branch checked out where '
              'available.\nSETUP COMPLETE')
