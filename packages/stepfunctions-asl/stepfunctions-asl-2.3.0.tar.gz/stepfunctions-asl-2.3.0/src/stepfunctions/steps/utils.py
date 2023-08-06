# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.
from __future__ import absolute_import

import logging
from stepfunctions.inputs import Placeholder

logger = logging.getLogger('asl')


def tags_dict_to_kv_list(tags_dict):
    kv_list = [{"Key": k, "Value": v} for k, v in tags_dict.items()]
    return kv_list


def get_aws_partition():

    """
    Returns the aws partition for the current AWS session.
    Defaults to 'aws' if the region could not be detected.
    """

    logger.warning("AWS session is not supported. Using default partition: aws")
    return "aws"


def merge_dicts(target, source):
    """
    Merges source dictionary into the target dictionary.
    Values in the target dict are updated with the values of the source dict.
    Args:
        target (dict): Base dictionary into which source is merged
        source (dict): Dictionary used to update target. If the same key is present in both dictionaries, source's value
             will overwrite target's value for the corresponding key
    """
    if isinstance(target, dict) and isinstance(source, dict):
        for key, value in source.items():
            if key in target:
                if isinstance(target[key], dict) and isinstance(source[key], dict):
                    merge_dicts(target[key], source[key])
                elif target[key] == value:
                    pass
                else:
                    logger.info(
                        f"Property: <{key}> with value: <{target[key]}>"
                        f" will be overwritten with provided value: <{value}>")
                    target[key] = source[key]
            else:
                target[key] = source[key]
