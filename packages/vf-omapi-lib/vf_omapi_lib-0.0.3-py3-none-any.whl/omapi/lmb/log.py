import json
import logging
import os

from omapi.lmb import lmb_config


class FormatterJSON(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        j = {
            "levelname": record.levelname,
            "time": "%(asctime)s.%(msecs)dZ"
            % dict(asctime=record.asctime, msecs=record.msecs),
            "aws_request_id": getattr(
                record, "aws_request_id", "00000000-0000-0000-0000-000000000000"
            ),
            "message": record.message,
            "module": record.module,
            "extra_data": record.__dict__.get("data", {}),
        }
        return json.dumps(j)


def init_logger(use_json_formatter=True):
    formatter = FormatterJSON(
        "[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n",
        "%Y-%m-%dT%H:%M:%S",
    )

    logger = logging.getLogger()
    # Replace the LambdaLoggerHandler formatter
    if use_json_formatter:
        logger.handlers[0].setFormatter(formatter)

    # try to set log-level out of the Lambda-Env-Variables (set by TF)
    envvar_key_loglevel = lmb_config["envvar.key.logging.lvl"]
    try:
        logger.setLevel(os.environ[envvar_key_loglevel])
    except RuntimeError as err:
        logger.warning(
            "could not get set log-level by env-variable %s; defaulting to INFO",
            envvar_key_loglevel,
            err,
        )
        logger.setLevel("INFO")
