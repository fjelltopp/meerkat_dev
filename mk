#!/usr/bin/env python2
from util import dev_accounts
import util
import argparse
import sys


# ARGUMENT PARSING ------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='This script provides a variety of tools for managing the '
                'Meerkat development environment. Get started with `mk setup`.'
)
subparsers = parser.add_subparsers(
    title='Actions',
    description='Choose which action to take.',
    metavar='action',
    dest='action'
)
actions = {}

# Add the setup command arguments
actions['setup'] = subparsers.add_parser(
    'setup',
    description='Sets up the Meerkat code base locally',
    help='Sets up the Meerkat codebase locally (Google repo).',
)
actions['setup'].add_argument(
    '-a', '--all',
    help='Download the complete development environment, including secure '
         'country config repos - N.B. you will need special access to be '
         'granted by the Meerkat Administrators to use this setup.',
    action='store_true'
)
actions['setup'].set_defaults(func=util.setup)

actions['init'] = subparsers.add_parser(
    'init',
    description="Initializes Meerkat Code project and google repo.",
    help="Configures the already existing Meerkat codebase with already checkout repositories (Google repo)."
)
actions['init'].set_defaults(func=util.init)

actions['init'].add_argument(
    '-a', '--all',
    help='Initialize the complete development environment, including secure '
         'country config repos',
    action='store_true'
)

# Add the Google repo command arguments
actions['sync'] = subparsers.add_parser(
    'sync',
    description='Runs the Google Repo "sync" command',
    help='Sync the Meerkat code base with Github (Google Repo)',
    add_help=False
)
actions['sync'].set_defaults(func=util.run_repo)

actions['status'] = subparsers.add_parser(
    'status',
    description='Runs the Google Repo "status" command',
    help='Print out the Git status messages for all Meerkat Git repositories '
         '(Google repo)',
    add_help=False
)
actions['status'].set_defaults(func=util.run_repo)

actions['diff'] = subparsers.add_parser(
    'diff',
    description='Runs the Google Repo "" command',
    help='View the Git diff messages for all Meerkat Git repositories '
         '(Google repo)',
    add_help=False
)
actions['diff'].set_defaults(func=util.run_repo)

actions['forall'] = subparsers.add_parser(
    'forall',
    description='Runs the Google Repo "forall" command',
    help='Run a shell command in all Git repositories (Google repo)',
    add_help=False
)
actions['forall'].set_defaults(func=util.run_repo)

actions['repo'] = subparsers.add_parser(
    'repo',
    description='Run any Google repo command',
    help='Run any Google Repo command',
    add_help=False
)
actions['repo'].set_defaults(func=util.run_repo)

# The db dump argument parsing
actions['dump'] = subparsers.add_parser(
    'dump',
    description='Dumps the current database into a file',
    help='Dumps the current Meerkat database into a file'
)
actions['dump'].set_defaults(func=util.dump)
actions['dump'].add_argument(
    '-l', '--list',
    help='List existing dumps',
    action='store_true'
)
actions['dump'].add_argument(
    '-t', '--tag',
    help='An optional tag to attach to the dump filename'
)

# The developers accounts scripts
actions['users'] = subparsers.add_parser(
    'users',
    description="A script that stores and administers personal "
                "details about the developer so that tailored auth and hermes "
                "accounts can be created in the dev environment.  These "
                "details are ignored by github and only stored locally.",
    help='Creates a new dev user, enabling the user to receive slack, '
         'email & sms notifications'
)
actions['users'].set_defaults(func=dev_accounts.users)
users_parser = actions['users'].add_subparsers(
    title="What would you like to do?",
    metavar='action',
    dest='action'
)
users_parser.add_parser(
    'list',
    help='List the currently existing developer\'s accounts.',
)
users_parser.add_parser(
    'clear',
    help='Clear all developer\'s accounts.',
)
users_parser.add_parser(
    'add',
    help='Add a new developer account.',
)
users_parser.add_parser(
    'remove',
    help='Remove a developer account.',
)

# Docker compose
actions['up'] = actions['dc'] = subparsers.add_parser(
    'up',
    description="Start docker containers (docker-compose).",
    help="Start docker containers (docker-compose)."
)
actions['up'].set_defaults(func=util.up)
actions['up'].add_argument(
    'country',
    help='Specify the country to start e.g. jordan.',
    const='',
    nargs='?'
)
actions['up'].add_argument(
    '-db', '--db-dump',
    help='Use a db dump.',
)
actions['up'].add_argument(
    '-fd', '--fake-data',
    help='Use fake data instead of real data.',
    action='store_true'
)
actions['up'].add_argument(
    '-f', '--data-fraction',
    help='Use the specified fraction of the real data.',
)
actions['up'].add_argument(
    '-e', '--env',
    help='Specify an Env Variable e.g. -e ENV_VAR=value ',
    action='append'
)

actions['stop'] = subparsers.add_parser(
    'stop',
    description="Stop docker containers (docker-compose).",
    help="Stop docker containers (docker-compose)."
)
actions['stop'].set_defaults(func=util.run_docker_compose)

actions['restart'] = subparsers.add_parser(
    'restart',
    description="Restart docker containers (docker-compose).",
    help="Restart docker containers (docker-compose)."
)
actions['restart'].set_defaults(func=util.run_docker_compose)

actions['build'] = subparsers.add_parser(
    'build',
    description="Restart docker containers (docker-compose).",
    help="Restart docker containers (docker-compose)."
)
actions['build'].set_defaults(func=util.run_docker_compose)

actions['logs'] = subparsers.add_parser(
    'logs',
    description="Open the logs for a service (docker-compose)",
    help="Open the logs for a service (docker-compose)"
)
actions['logs'].set_defaults(func=util.run_docker_compose)

actions['dc'] = subparsers.add_parser(
    'dc',
    description="Run any docker-compose command.",
    help='Run any docker-compose command'
)
actions['dc'].set_defaults(func=util.run_docker_compose)

actions['exec'] = subparsers.add_parser(
    'exec',
    description="Run any docker-compose exec command.",
    help='Run any docker-compose exec command.'
)
actions['exec'].set_defaults(func=util.run_docker_compose)

# Docker exec bash
actions['bash'] = subparsers.add_parser(
    'bash',
    description="Open a bash prompt in the specified container.",
    help='Open a bash prompt in the specified container'
)
actions['bash'].set_defaults(func=util.run_docker_compose)
actions['bash'].add_argument('container', metavar='container', type=str,
                             help='The service name e.g."frontend."')


def main(orig_args):
    # Parse both args we recognise
    args, extra_args = parser.parse_known_args(orig_args)
    if hasattr(args, 'func'):
        # Parse the args!
        args.func(args, extra_args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main(sys.argv[1:])
