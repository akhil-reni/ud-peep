# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace


def parse_args() -> Namespace:
    """ Parses the args from command line
    Returns:
        Namespace: Returns known parsed arguments
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-o",
        metavar='Output',
        dest='Output',
        required=False,
        type=str,
        help="Output file for CSV")

    parser.add_argument(
        "-r",
        metavar='RoleArn',
        dest='RoleArn',
        required=False,
        type=str,
        help="Role ARN if you want to switch account")

    parser.add_argument(
        "-s",
        metavar='RoleSessionName',
        dest='RoleSessionName',
        required=False,
        type=str,
        help="Role session if you want to switch account")

    args = parser.parse_args()

    return args
