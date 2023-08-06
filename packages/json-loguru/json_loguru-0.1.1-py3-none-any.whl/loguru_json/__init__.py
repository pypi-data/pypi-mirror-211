import sys

from loguru import logger, _defaults

from . import monkey
from .format import escape_format, escape_colorized, JSONFormatterBuilder

logger.remove()


def _lower_level(level):
    return f"\"{level.name.lower()}\""


def _process_formatter(process):
    return f"\"{process.name}-{process.id}\""


def _thread_formatter(thread):
    return f"\"{thread.name}-{thread.id}\""


def add(sink,
        *,
        level=_defaults.LOGURU_LEVEL,
        format=_defaults.LOGURU_FORMAT,
        filter=_defaults.LOGURU_FILTER,
        backtrace=_defaults.LOGURU_BACKTRACE,
        diagnose=_defaults.LOGURU_DIAGNOSE,
        enqueue=_defaults.LOGURU_ENQUEUE,
        catch=_defaults.LOGURU_CATCH,
        **kwargs):
    return logger.add(sink, level=level, format=format, filter=filter, colorize=False, serialize=False,
                      backtrace=backtrace, diagnose=diagnose, enqueue=enqueue, catch=catch, **kwargs)


with JSONFormatterBuilder(display_process=True, process_formatter=_process_formatter, display_thread=True,
                          thread_formatter=_thread_formatter,
                          level_formatter=_lower_level) as formatter:
    _handler_id = add(sys.stdout, format=formatter,
                      level="DEBUG", backtrace=True, diagnose=True)


def remove():
    logger.remove(_handler_id)


__all__ = [
    logger,
    add,
    remove,
    escape_format,
    escape_colorized,
    JSONFormatterBuilder
]
