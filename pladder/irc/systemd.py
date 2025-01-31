import logging

from systemd.journal import JournalHandler  # type: ignore
from systemd.daemon import notify  # type: ignore

from pladder.irc.client import Hook


class SystemdHook(Hook):
    def __init__(self, config, client):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(JournalHandler(SYSLOG_IDENTIFIER="pladder-irc"))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def on_ready(self):
        notify("READY=1")

    def on_message_received(self):
        notify("WATCHDOG=1")

    def on_privmsg(self, timestamp, channel, sender, text):
        notify("WATCHDOG=1")

    def on_status(self, status):
        notify("STATUS=" + status)
