#!/usr/bin/python2
from util import dev_accounts
import util
import argparse
import sys


# ARGUMENT PARSING ------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='This script provides a variety of tools for managing the '
                'Meerkat development environment. Get started with `mk init`.'
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
    help='Sets up the Meerkat codebase locally (uses Google repo).',
)
actions['setup'].add_argument(
    '-a', '--all',
    help='Download the complete development environment, including secure '
         'country config repos - N.B. you will need special access to be '
         'granted by the Meerkat Administrators to use this setup.',
    action='store_true'
)
actions['setup'].set_defaults(func=util.setup)

# Add the Google repo command arguments
actions['sync'] = subparsers.add_parser(
    'sync',
    description='Runs the Google Repo "sync" command',
    help='Sync the entire Meerkat code base with Github (uses Google Repo)',
    add_help=False
)
actions['sync'].set_defaults(func=util.run_repo)

actions['status'] = subparsers.add_parser(
    'status',
    description='Runs the Google Repo "status" command',
    help='Print out the Git status messages for all Meerkat Git repositories '
         '(uses Google repo)',
    add_help=False
)
actions['status'].set_defaults(func=util.run_repo)

actions['diff'] = subparsers.add_parser(
    'diff',
    description='Runs the Google Repo "" command',
    help='Print out the Git diff messages for all Meerkat Git repositories '
         '(uses Google repo)',
    add_help=False
)
actions['diff'].set_defaults(func=util.run_repo)

actions['forall'] = subparsers.add_parser(
    'forall',
    description='Runs the Google Repo "forall" command',
    help='Runs the specified command for all Meerkat repositories (uses '
         'Google repo)',
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
         'email and text notifications from the development environment.'
)
actions['users'].set_defaults(func=dev_accounts.users)
actions['users'].add_argument(
    '--list',
    help='List the currently existing developer\'s accounts.',
    action='store_true'
)
actions['users'].add_argument(
    '--clear',
    help='Clear all developer\'s accounts.',
    action='store_true'
)
actions['users'].add_argument(
    '--add',
    help='Add a new developer account.',
    action='store_true'
)
actions['users'].add_argument(
    '--remove',
    help='Remove a developer account.',
    action='store_true'
)


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
