import tecerator as _tc
import atexit as _atexit
import argparse as _argparse

def build(args):
    target_name = args.target
    target = _tc.target.select(target_name)
    task = _tc.extraction.extract_main()
    target.build(task)

def run():
    parser = _argparse.ArgumentParser(prog='tecerator')
    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser('build')
    parser_build.add_argument('--target', choices=_tc.target.TARGET_CLI_NAMES, required=True)
    parser_build.set_defaults(func=build)

    args = parser.parse_args()
    args.func(args)

_atexit.register(run)