"""Usage:
  packit start <path> [--extra=PATH] [--option=OPTION]... [--pull]
  packit status <path>
  packit stop <path> [--volumes] [--network] [--kill] [--force]
    [--extra=PATH] [--option=OPTION]...

Options:
  --extra=PATH     Path, relative to <path>, of yml file of additional
                   configuration
  --option=OPTION  Additional configuration options, in the form key=value
                   Use dots in key for hierarchical structure, e.g., a.b=value
                   This argument may be repeated to provide multiple arguments
  --pull           Pull images before starting
  --volumes        Remove volumes (WARNING: irreversible data loss)
  --network        Remove network
  --kill           Kill the containers (faster, but possible db corruption)
"""

import docopt
import yaml


from packit_deploy.config import PackitConfig
from packit_deploy.packit_constellation import packit_constellation


def main(argv=None):
    args = docopt.docopt(__doc__, argv)
    extra = args["--extra"]
    options = parse_option(args)
    path = args["<path>"]
    cfg = PackitConfig(path, extra, options)
    obj = packit_constellation(cfg)
    if args["start"]:
        packit_start(obj, args)
    elif args["status"]:
        packit_status(obj)
    elif args["stop"]:
        packit_stop(obj, args, cfg)
    return True

def packit_start(obj, args):
    pull_images = args["--pull"]
    obj.start(pull_images=pull_images)


def packit_status(obj):
    obj.status()


def packit_stop(obj, args, cfg):
    verify_data_loss(args, cfg)
    kill = args["--kill"]
    network = args["--network"]
    volumes = args["--volumes"]
    obj.stop(kill, remove_network=network, remove_volumes=volumes)


def verify_data_loss(args, cfg):
    if args["--volumes"]:
        if cfg.protect_data:
            raise Exception("Cannot remove volumes with this configuration")
        else:
            print("""WARNING! PROBABLE IRREVERSIBLE DATA LOSS!

You are about to delete the data volumes. This action cannot be undone
and will result in the irreversible loss of *all* data associated with
the application. This includes all databases, packet data etc.""")

            if not prompt_yes_no():
                raise Exception("Not continuing")


def prompt_yes_no(get_input=input):
    return get_input("\nContinue? [yes/no] ") == "yes"


def parse_option(args):
    return [string_to_dict(x) for x in args["--option"]]


def string_to_dict(string):
    """Convert a configuration option a.b.c=x to a dictionary
{"a": {"b": "c": x}}"""
    # Won't deal with dots embedded within quotes but that's ok as
    # that should not be allowed generally.
    try:
        key, value = string.split("=")
    except ValueError:
        msg = "Invalid option '{}', expected option in form key=value".format(
            string)
        raise Exception(msg)
    value = yaml_atom_parse(value)
    for k in reversed(key.split(".")):
        value = {k: value}
    return value


def yaml_atom_parse(x):
    ret = yaml.load(x, Loader=yaml.Loader)
    if type(ret) not in [bool, int, float, str]:
        raise Exception("Invalid value '{}' - expected simple type".format(x))
    return ret
