#!/usr/bin/env python3

from pathlib import Path

from pyclui import Logger, INFO

logger = Logger(__name__, INFO, Path(__file__).parent/'log')
logger.debug('asdfs %d\nasdfssadfasdfas\ndasasdf', 1)
logger.debug("".format(21341234))
logger.info('I told you so %d\nkjlhkljhjkjkh', 1)
logger.warning('Watch out!')
logger.error("an error occurrence！\nsdfasfd")
logger.critical('asdf')
