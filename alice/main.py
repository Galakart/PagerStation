"""Main Alice skill handler"""
import logging

import enums
import handlers
from pythonjsonlogger import jsonlogger


class YcLoggingFormatter(jsonlogger.JsonFormatter):
    """Класс логов для Y.Cloud"""

    def add_fields(self, log_record, record, message_dict):
        super(YcLoggingFormatter, self).add_fields(log_record, record, message_dict)
        log_record['logger'] = record.name
        log_record['level'] = str.replace(
            str.replace(record.levelname, "WARNING", "WARN"),
            "CRITICAL",
            "FATAL"
        )


logHandler = logging.StreamHandler()
logHandler.setFormatter(YcLoggingFormatter('%(message)s %(level)s %(logger)s'))
logger = logging.getLogger()
logger.propagate = False
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)


def handle_event(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    # logger.info("My log message", extra={"my-key": "my-value"})

    if event['session']['new']:
        return handlers.handle_start(event=event)

    if 'state' not in event or 'step_number' not in event['state']['session']:
        return handlers.handle_something_wrong(event=event)

    match event['state']['session']['step_number']:
        case enums.StatesEnum.ASK_ID_PAGER:
            return handlers.handle_id_pager(event=event)

        case enums.StatesEnum.ASK_MESSAGE:
            return handlers.handle_message(event=event)
