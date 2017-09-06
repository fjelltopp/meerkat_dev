#!/usr/bin/python2

import argparse
import util
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
    description='Dumps the current database into the specified file',
    help='Dumps the current Meerkat database into the specified file',
    add_help=False
)
actions['dump'].set_defaults(func=util.dump)


def main(orig_args):
    # Parse both args we recognise
    args, extra_args = parser.parse_known_args()

    if hasattr(args, 'func'):
        # Parse the args!
        args, extra_args = parser.parse_known_args()
        args.func(args, extra_args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main(sys.argv[1:])
