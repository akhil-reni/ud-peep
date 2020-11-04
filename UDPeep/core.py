# -*- coding: utf-8 -*-
import boto3
from argparse import Namespace
from typing import List
import base64
import re
import csv

from UDPeep.logging import get_logger
from UDPeep.exceptions import AWSAssumeException
from UDPeep.enums import REGEX_LIST


logger = get_logger()


def get_boto_client(arguments: Namespace) -> boto3.client:
    try:
        if arguments.RoleArn and arguments.RoleSession:
            logger.info("[!] Switching account...")
            sts_client = boto3.client('sts')
            assumed_role_object = sts_client.assume_role(
                RoleArn="arn:aws:iam::account-of-role-to-assume:role/name-of-role",
                RoleSessionName="AssumeRoleSession1")
            credentials = assumed_role_object.get('Credentials', None)
            if credentials:
                client = boto3.client(
                    'ec2',
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'],
                    aws_session_token=credentials['SessionToken'],
                )
                return client
            else:
                raise AWSAssumeException
        else:
            logger.info("[!] Using default account...")
            client = boto3.client('ec2')
            return client
    except Exception as e:
        logger.error(e)
        raise e


def get_instances_list(client: boto3.client) -> List[str]:
    logger.info("[!] Getting list of instances...")
    instances_list = []
    instances = client.describe_instances()
    for instance in instances["Reservations"]:
        for i in instance["Instances"]:
            instances_list.append(i.get("InstanceId", None))
    logger.info(f"[!] Found {len(instances_list)} instances.")
    return instances_list


def get_user_data(client: boto3.client,
                  instances_list: List[str]) -> List[dict]:
    logger.info("[!] Fetching user data attached to the instances...")
    user_data_list = []
    for instance in instances_list:
        instance_dict = dict()
        instance_dict["id"] = instance
        instance_dict["user_data"] = client.describe_instance_attribute(
            InstanceId=instance, Attribute="userData")
        user_data_list.append(instance_dict)
    return user_data_list


def find_secrets(user_data_list: List[dict]) -> List[dict]:
    logger.info("[!] Scanning for secrets...")
    results = []
    for user_data in user_data_list:
        ud = user_data.get("user_data").get('UserData').get("Value", None)
        if ud:
            ud = base64.b64decode(ud).decode()
            for k, v in REGEX_LIST.items():
                found = re.findall(v, x)
                if len(found) > 0:
                    for r in found:
                        logger.info(
                            f"[+] Secret key found, Instance ID: {user_data['id']}, Pattern {k}, value: {''.join(r)}")
                        user_data["pattern"] = ''.join(r)
                        results.append(user_data)
    return results


def write_to_csv(results: List[dict], filename: str) -> None:
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
