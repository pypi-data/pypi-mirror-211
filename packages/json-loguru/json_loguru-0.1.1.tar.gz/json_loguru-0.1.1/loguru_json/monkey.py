import io
import json

from loguru._handler import Message

from .json_encoder import CustomJSONEncoder


def _patch_message(message):
    sb = io.StringIO()
    record = message.record
    first_line, *traceback = message.split("\n")
    sb.write(first_line)

    if traceback:
        sb.write(", ")
        sb.write("\"exception\":")
        str_traceback = json.dumps("\n".join(traceback), cls=CustomJSONEncoder, ensure_ascii=False)
        sb.write(str_traceback)

    sb.write("}")
    sb.write("\n")
    new_message = Message(sb.getvalue())
    new_message.record = record
    sb.close()
    return new_message


def _patch_file_sink():
    from loguru._file_sink import FileSink
    write = FileSink.write

    def _file_sink_write(self, message):
        new_message = _patch_message(message)
        write(self, new_message)

    FileSink.write = _file_sink_write


def _patch_stream_sink():
    from loguru._simple_sinks import StreamSink
    write = StreamSink.write

    def _stream_sink_write(self, message):
        new_message = _patch_message(message)
        write(self, new_message)

    StreamSink.write = _stream_sink_write


def _patch_standard_sink():
    from loguru._simple_sinks import StandardSink
    write = StandardSink.write

    def _standard_sink_write(self, message):
        new_message = _patch_message(message)
        write(self, new_message)

    StandardSink.write = _standard_sink_write


def _patch_async_sink():
    from loguru._simple_sinks import AsyncSink
    write = AsyncSink.write

    def _async_sink_write(self, message):
        new_message = _patch_message(message)
        write(self, new_message)

    AsyncSink.write = _async_sink_write


def _patch_callable_sink():
    from loguru._simple_sinks import CallableSink
    write = CallableSink.write

    def _callable_sink_write(self, message):
        new_message = _patch_message(message)
        write(self, new_message)

    CallableSink.write = _callable_sink_write


def _patch():
    _patch_file_sink()
    _patch_stream_sink()
    _patch_standard_sink()
    _patch_async_sink()
    _patch_callable_sink()


_patch()
