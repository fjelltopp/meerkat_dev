import repo
import subprocess
import os
import sys
from datetime import datetime

# Some settings
MANIFEST_URL = "git@github.com:meerkat-code/meerkat.git"
DEV_MANIFEST = 'dev.xml'
DEMO_MANIFEST = 'default.xml'
DUMPS_PATH = (os.path.abspath(os.path.dirname(__file__)) +
              "/../.settings/dumps/")
COMPOSE_PATH = (os.path.abspath(os.path.dirname(__file__)) +
                "/../compose/")


def call_command(args):
    """
    Run a shell command with proper error logging.
    """
    try:
        retcode = subprocess.call(
            ' '.join(args),
            shell=True,
            cwd=COMPOSE_PATH
        )
        if retcode is not 0:
            print >>sys.stderr, "Command not successful. Returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e


def up(args, extra_args):
    """
    Start the dev_env.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user.
    """
    # Export environment variables for dev_env options.
    env = []
    if args.fake_data:
        env += ['export', 'NEW_FAKE_DATA=1', '&&']
        env += ['export', 'GET_DATA_FROM_S3=0', '&&']
    if args.data_fraction:
        env += ['export', 'IMPORT_FRACTION=' + args.data_fraction, '&&']
    if args.db_dump:
        filename = DUMPS_PATH + args.db_dump
        if args.db_dump and not os.path.isfile(filename):
            raise Exception("DB DUMP file does not exist.")
        else:
            env += ['export', 'DB_DUMP=' + filename, '&&']
    if args.env:
        for var in args.env:
            env += ['export', var, '&&']

    # Build the complete command
    compose = ['docker-compose']
    if args.country:
        compose += ["-f", args.country + '.yml']
    up = ["up", "-d"] + extra_args
    command = '"{}"'.format(' '.join(env + compose + up))

    # Run the command
    call_command(['sudo', 'sh', '-c', command])


def run_docker_compose(args, extra_args):
    """
    Run's a docker compose command in the compose folder.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    if args.action == 'dc':
        call_command(["sudo", "docker-compose"] + extra_args)
    if args.action == 'logs':
        call_command(["sudo", "docker-compose", "logs", "-f"] + extra_args)
    else:
        call_command(["sudo", "docker-compose", args.action] + extra_args)


def run_docker_exec(args, extra_args):
    """
    Run's a docker exec command.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    call_command(["sudo", "/usr/bin/docker", "exec"] + extra_args)


def bash(args, extra_args):
    """
    Opens a bash prompt in the specified container.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    # Get the container prefix from the compose path and build container name
    prefix = filter(None, COMPOSE_PATH.split("/"))[-1]

    # Allow user to specify service or compleate container name
    container = args.container
    if prefix not in container:
        container = ''.join([prefix, '_', args.container, "_1"])

    # Run the bash command
    call_command(
        ["sudo", "/usr/bin/docker", "exec", "-ti", container, "bash"]
    )


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
    call_command([
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
        manifest = DEV_MANIFEST if args.all else DEMO_MANIFEST
        repo.main(['init', '-u', MANIFEST_URL, '-m', manifest, '--return'])
        repo.main(['sync', '--force-sync', '--return'])
        print('Meerkat code synced')
        repo.main(['forall', '-c', 'git', 'checkout', 'master', '--return'])
        try:
            repo.main(['forall', '-c', 'git', 'checkout',
                       '-q', 'development', '--return'])
        except subprocess.CalledProcessError:
            print('Some repos do not have a development branch.')

        print('Master and Development branches created on your '
              'local machine.\nDevelopment branch checked out where '
              'available.')
        repo.main(['status', '--return'])
        print('--SETUP COMPLETE--')
