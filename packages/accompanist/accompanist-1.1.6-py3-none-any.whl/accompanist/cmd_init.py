import json

import click

import accompanist.utility as ut

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(name="init", context_settings=CONTEXT_SETTINGS,
               help="Configure CWL log group setting.")
@click.option("-l", "--log-group", required=True, default="aws-waf-logs-xxxxxxx", type=str,
              prompt="Please input a log group name",
              help="Set a CloudWatch Logs Log group name.")
@click.option("-p", "--path", required=True, default="/.env", type=str,
              prompt="Please input a analysis target URI path",
              help="Set a URI path for counts that is blocked/counted.")
@click.option("-c", "--comment", required=True,
              default="This is a sample comment.", type=str,
              prompt="Please input a comment on the report",
              help="Set a comment for report.")
def init(log_group: str, path: str, comment: str) -> None:

    configure_items = {
        "log_group": log_group,
        "target_uri": [path],
        "comment": [comment]
    }

    with open("config.json", mode="w", encoding="utf-8") as f:
        json.dump(configure_items, f, indent=2)

    info_config = "\n[Info] A configuration file \"config.json\" is generated!"
    info_omitted = "[Info] The other path names and comment can also be added optionally by editing that file. They were omitted in this automatically initialized process.\n"
    ut.colorize_print(info_config, "cyan")
    ut.colorize_print(info_omitted, "cyan")
