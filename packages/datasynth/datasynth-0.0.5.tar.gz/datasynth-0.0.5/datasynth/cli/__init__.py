import logging
import os

import click
import gytrash

from . import commands

log = logging.getLogger("datasynth")


if "SYSTEM__GYTRASH_BOT_TOKEN" in os.environ:
    SYSTEM_GYTRASH_BOT_TOKEN = os.environ["SYSTEM__GYTRASH_BOT_TOKEN"]
else:
    SYSTEM_GYTRASH_BOT_TOKEN = ""

if "SYSTEM__GYTRASH_SLACK_LOG_LEVEL" in os.environ:
    SYSTEM_GYTRASH_SLACK_LOG_LEVEL = os.environ["SYSTEM__GYTRASH_SLACK_LOG_LEVEL"]
else:
    SYSTEM_GYTRASH_SLACK_LOG_LEVEL = None

if "SYSTEM__GYTRASH_SLACK_CHANNEL" in os.environ:
    SYSTEM_GYTRASH_SLACK_CHANNEL = os.environ["SYSTEM__GYTRASH_SLACK_CHANNEL"]
else:
    SYSTEM_GYTRASH_SLACK_CHANNEL = ""

if "SYSTEM__GYTRASH_SLACK_ENABLE" in os.environ:
    SYSTEM_GYTRASH_SLACK_ENABLE = os.environ["SYSTEM__GYTRASH_SLACK_ENABLE"]
else:
    SYSTEM_GYTRASH_SLACK_ENABLE = False


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    help="Supply once to display debug logs.",
)
@click.option(
    "--silent",
    is_flag=True,
    help="Supply once to silence all log messages.",
)
@click.option(
    "--botocore",
    is_flag=True,
    help="Supply to display Botocore debug logs.",
)
@click.option(
    "--slack",
    default=SYSTEM_GYTRASH_SLACK_ENABLE,
    help="Supply to log to Slack.",
)
@click.option(
    "--slack-log-level",
    default=SYSTEM_GYTRASH_SLACK_LOG_LEVEL,
    help="Supply once to display Botocore debug logs.",
)
@click.option(
    "--slack-log-channel",
    default=SYSTEM_GYTRASH_SLACK_CHANNEL,
    help="Supply once to display Botocore debug logs.",
)
@click.option(
    "--gytrash-bot-token",
    default=SYSTEM_GYTRASH_BOT_TOKEN,
    help="Supply to connect to the Gytrash logger in slack.",
)
@click.option(
    "--output",
    default="text",
    help="Output format for dumping json payloads.",
)
@click.pass_context
def cli(
    ctx: click.core.Context,
    debug: bool,
    silent: bool,
    botocore: bool,
    slack: bool,
    slack_log_level: int,
    slack_log_channel: str,
    gytrash_bot_token: str,
    output: str,
):
    ctx.ensure_object(dict)

    log_level = 20

    if silent:
        log_level = 50
    else:
        if debug:
            log_level = 10

    if not slack_log_level:
        slack_log_level = log_level

    if str(slack) == "False":
        slack = False
    else:
        slack = True

    gytrash.setup_logging(
        log,
        log_level=log_level,
        log_from_botocore=botocore,
        log_to_slack=slack,
        slack_log_channel=slack_log_channel,
        slack_log_level=slack_log_level,
        slack_bot_token=gytrash_bot_token,
    )

    log.debug(f"Slack logging is: {slack}", extra={"notify_slack": True})

    ctx.obj["log"] = logging.getLogger("datasynth.cli")
    ctx.obj["output"] = output


for cmd in commands.__all__:
    cli.add_command(getattr(commands, cmd))
