#!/usr/bin/env python3
#
# logMaintenance.py

"""
Documentation:
  logMaintenance.py enters the arguments into the life.log with format:
  YYYY-MM-DD HH:MM:SS|[logMaintenance.main]|<string>
"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys

sys.path.append('/home/ubuntu/wali_desk/plib')
import lifeLog

from time import sleep


def main():
    args = sys.argv
    if (len(args) == 1):
          print('USAGE: ./logMaintenance.py "log this message to life.log"')
    else:
          strToLog = "** " + args[1] + " **"
          lifeLog.logger.info(strToLog)
          print("'{}' added to life.log".format(strToLog))
    sleep(1)


if (__name__ == '__main__'):  main()
