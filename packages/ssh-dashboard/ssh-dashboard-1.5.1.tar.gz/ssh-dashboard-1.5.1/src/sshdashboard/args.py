#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from .appversion import GetAppVersion

def GetArgParser() -> argparse.ArgumentParser:
    tArgParser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS].",
                                         description="SSH Linux host monitoring tool")
    tArgParser.add_argument("-v", "--version", help="Show version", action="version", version = f"{tArgParser.prog} version {GetAppVersion()}")
    tArgParser.add_argument("-c", "--config", help="Configuration file to use (default: ./config.json)", type=str, default="./config.json", required=False)
    tArgParser.add_argument("-d", "--verbose", help="Enable verbose log output", action="store_true")
    tArgParser.add_argument("-f", "--get_default_config", help="Copy a sample configuration file to the current directory and exit", action="store_true")
    return tArgParser
