"""Settings File for emails."""

import configparser

config = configparser.RawConfigParser()
config.read(r"config.toml")

MAIL_ITEM = 0

DISPLAY = config["INTERFACE"].getboolean("display")

TEST_EMAIL = config["TEST_DATA"]["email"]
