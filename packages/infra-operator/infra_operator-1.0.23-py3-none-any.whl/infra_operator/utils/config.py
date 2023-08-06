import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_commandline_args(args=None):
    global config
    parser = argparse.ArgumentParser(description='receive args')

    parser.add_argument('action',
                        choices=["create", "delete", "validate",
                                 "export", "export-ref", "diff", "render", "output"],
                        action='store',
                        type=str,
                        help='action')

    parser.add_argument('-t',
                        '--template',
                        action='store',
                        type=str,
                        required=True,
                        help='template file or directory')

    parser.add_argument('-v',
                        '--values',
                        action='store',
                        type=str,
                        required=False,
                        help='values file, should have single key `input`, optionally `output`. if not, the whole file is considered as variables.')

    parser.add_argument('-w',
                        '--write',
                        action='store',
                        type=str2bool,
                        nargs='?',
                        default=True,
                        const=True,
                        required=False,
                        help='-w y|-w n, When yes, export write to file')

    parser.add_argument('-n',
                        '--filename',
                        action='store',
                        type=str,
                        nargs='?',
                        default="",
                        const=True,
                        required=False,
                        help='override filename, used for testing')

    parsed = parser.parse_args(args=args)
    config = parsed
    return parsed


global config
