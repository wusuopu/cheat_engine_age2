#!/usr/bin/env python
# encoding: utf-8

import logging
import sys

logger = logging.Logger('')
logger.addHandler(logging.StreamHandler(sys.stdout))


def puts(log):
    logger.info(log)
