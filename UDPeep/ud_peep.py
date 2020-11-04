# -*- coding: utf-8 -*-
from UDPeep.logging import get_logger
from UDPeep.input import parse_args
from UDPeep.core import get_boto_client, get_instances_list, get_user_data, \
    find_secrets, write_to_csv

logger = get_logger()


def main():
    logger.info("[!] Running UD Peep...")
    arguments = parse_args()
    client = get_boto_client(arguments)
    instances_list = get_instances_list(client)
    user_data_list = get_user_data(client, instances_list)
    results = find_secrets(user_data_list)
    if arguments.Output and len(results) > 0:
        logger.info("[!] Writing output to CSV...")
        write_to_csv(results, arguments.Output)


if __name__ == "__main__":
    main()
