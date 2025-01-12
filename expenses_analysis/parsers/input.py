from argparse import ArgumentParser, BooleanOptionalAction


def input_parser(argv=None):

    parser = ArgumentParser()

    parser.add_argument("--version",
                        "-v",
                        action="version",
                        version="v0.0.1")

    parser.add_argument("--path",
                        type=str,
                        default=None,
                        help="Full path of the expenses file.")

    parser.add_argument("--save",
                        type=bool,
                        default=False,
                        action=BooleanOptionalAction,
                        help="Flag to save the results.")

    args = parser.parse_args(argv)

    return args
