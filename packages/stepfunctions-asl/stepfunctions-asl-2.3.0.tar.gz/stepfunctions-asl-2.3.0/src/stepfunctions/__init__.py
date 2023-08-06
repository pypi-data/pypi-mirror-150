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
import sys

__useragent__ = "aws-step-functions-data-science-sdk-python"

# disable logging.warning() from import packages
logging.getLogger().setLevel(logging.ERROR)

from stepfunctions import steps

def set_stream_logger(level=logging.INFO):
    logger = logging.getLogger('asl')
    # setup logger config
    logger.setLevel(level)
    logger.propagate = False
    # avoid attaching multiple identical stream handlers
    logger.handlers = []
    # add stream handler to logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    logger.addHandler(handler)

# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger('asl').addHandler(NullHandler())
