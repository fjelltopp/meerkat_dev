import os
import subprocess
import sys
from datetime import datetime

import repo
from util.dummy_aws_credentials import create_dummy_aws_config

# Some settings
# If you run docker with a sudo, set this envvar to the sudo command: 'sudo'
SUDO = os.environ.get('MEERKAT_SUDO', '')
# If you want to fetch containers using https, you should set this env var to
# https://github.com/meerkat-code/meerkat.git
MANIFEST_URL = os.environ.get(
    'MEERKAT_MANIFEST',
    'git@github.com:fjelltopp/meerkat.git'
)
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
        print(' '.join(args).strip())
        retcode = subprocess.call(
            ' '.join(args).strip(),
            shell=True,
            cwd=COMPOSE_PATH
        )
        if retcode is not 0:
            print >> sys.stderr, "Command not successful. Returned", retcode
    except OSError as e:
        print >> sys.stderr, "Execution failed:", e


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
        env += ['export', 'INITIAL_DATA_SOURCE=FAKE_DATA', '&&']
        env += ['export', 'STREAM_DATA_SOURCE=NO_STREAMING', '&&']
    if args.fake_real_time:
        env += ['export', 'INITIAL_DATA_SOURCE=AWS_S3', '&&']
        env += ['export', 'FAKE_DATA_GENERATION=INTERNAL', '&&']
        env += ['export', 'STREAM_DATA_SOURCE=NO_STREAMING', '&&']
    if args.csv:
        env += ['export', 'INITIAL_DATA_SOURCE=LOCAL_CSV', '&&']
        env += ['export', 'STREAM_DATA_SOURCE=NO_STREAMING', '&&']
    if args.start_date:
        env += ['export', 'ONLY_IMPORT_AFTER=' + args.start_date, "&&"]
    if args.data_proportion:
        env += ['export', 'IMPORT_FRACTION=' + args.data_proportion, '&&']
    if args.db_dump:
        filename = DUMPS_PATH + args.db_dump
        if args.db_dump and not os.path.isfile(filename):
            raise Exception("DB DUMP file does not exist.")
        else:
            env += ['export', 'DB_DUMP=' + args.db_dump, '&&']
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
    call_command([SUDO, 'sh', '-c', command])


def run_docker_compose(args, extra_args):
    """
    Run's a docker compose command in the compose folder. Is used for the
    dc, exec, logs, bash, stop, restart commands.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    if args.action == 'dc':
        call_command([SUDO, "docker-compose"] + extra_args)
    elif args.action == 'exec':
        call_command([SUDO, "docker-compose", "exec"] + extra_args)
    elif args.action == 'logs':
        call_command([SUDO, "docker-compose", "logs", "-f"] + extra_args)
    elif args.action == 'bash':
        call_command([SUDO, "docker-compose", "exec", args.container, "bash"])
    else:
        call_command([SUDO, "docker-compose", args.action] + extra_args)


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
    cmd = [SUDO] if SUDO else []
    cmd += ["docker", "exec", "-ti",
            "compose_db_1", "sh", "-c", "echo \"$COUNTRY\""]
    country = subprocess.check_output(cmd).strip()

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
    cmd = [SUDO] if SUDO else []
    cmd += ["docker", "exec", "-ti", "compose_db_1", "sh", "-c",
            "\"pg_dump -U postgres -h localhost meerkat_db\" > " + filename]
    call_command(cmd)


def init(args, extra):
    print("Initializing the Meerkat codebase...")
    manifest = DEV_MANIFEST if args.all else DEMO_MANIFEST
    repo.main(['init', '-u', MANIFEST_URL, '-m', manifest])
    print("Meerkat initialized")
    print("Meerkat status:")
    repo.main(['status'])


def setup(args, extra):
    """
    Initialises the parent directory to be the Meerkat code base folder.
    Optionally specify which manifest to use.
    """
    print('Setting up the Meerkat codebase...')
    print('This will destroy changes, resetting everything to the remote.')

    if raw_input('ARE YOU SURE YOU WANT TO CONTINUE? (y/N) ') in ['Y', 'y', 'yes', 'Yes', 'YES']:
        create_dummy_aws_config()
        manifest = DEV_MANIFEST if args.all else DEMO_MANIFEST
        repo.main(['init', '-u', MANIFEST_URL, '-m', manifest])
        repo.main(['sync', '--force-sync'])
        print('Meerkat code synced')
        repo.main(['forall', '-c', 'git', 'checkout', 'master'])
        try:
            repo.main(['forall', '-c', 'git', 'checkout',
                       '-q', 'development'])
        except subprocess.CalledProcessError:
            print('Some repos do not have a development branch.')

        print('Master and Development branches created on your '
              'local machine.\nDevelopment branch checked out where '
              'available.')
        repo.main(['status'])
        print('--SETUP COMPLETE--')
