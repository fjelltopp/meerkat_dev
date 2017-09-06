import repo
import subprocess

DB_DUMPS_FOLDER = "./abacus/dumps/"

def run_repo(args, extra_args):
    """
    Run's a Google Repo command by just forwarding the supplied args to the
    main() function of the Google Repo script.

    Args:
        args (NameSpace): The known args NameSpace object returned by argsparse
        extra_args ([str]): A list of strings detailing any extra unkown args
            supplied by the user
    """
    print(args.action)
    if args.action == "repo":
        print(extra_args)
        repo.main(extra_args)
    else:
        repo.main([args.action] + extra_args)


def dump(args, extra_args):
    filename = DB_DUMPS_FOLDER + "test_dump"

    # Get the dump by executing pg_dump in the db container
    # Executing in container ensures same client and server version of pg_dump
    subprocess.check_output([
        "sh", "-c",
        "sudo docker exec -ti compose_db_1 sh -c "
        "\"pg_dump -U postgres -h localhost meerkat_db\" > " + filename
    ])
