import io
import json

from .json_encoder import CustomJSONEncoder


def escape_format(target):
    return target.replace("{", "{{").replace("}", "}}")


def escape_colorized(target):
    # return target
    return target.replace("<", "\\<")


class JSONFormatterBuilder:
    def __init__(self, display_elapsed=False, elapsed_formatter=None, display_file=True, file_formatter=None,
                 display_function=False, level_formatter=None, display_line=True, display_module=False,
                 display_name=False, display_process=False, process_formatter=None, display_thread=False,
                 thread_formatter=None, display_time=True, time_format="YYYY-MM-DD HH:mm:ss"):
        self._display_elapsed = display_elapsed
        self._elapsed_formatter = elapsed_formatter

        self._display_file = display_file
        self._file_formatter = file_formatter

        self._display_function = display_function

        self._lever_formatter = level_formatter

        self._display_line = display_line

        self._display_module = display_module

        self._display_name = display_name

        self._display_process = display_process
        self._process_formatter = process_formatter

        self._display_thread = display_thread
        self._thread_formatter = thread_formatter

        self._display_time = display_time
        if time_format == "":
            time_format = "YYYY-MM-DD HH:mm:ss"
        self._time_format = time_format

        self._sb = None

    def __enter__(self):
        return self._build()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._sb is not None:
            self._sb.close()
        return False

    def _build(self):
        def formatter(record):
            self._sb = io.StringIO()
            self._sb.write("{{")
            self._build_level(record)
            self._build_time()
            self._build_elapsed(record)
            self._build_process(record)
            self._build_thread(record)
            self._build_file(record)
            self._build_line(record)
            self._build_function(record)
            self._build_module(record)
            self._build_name(record)
            self._build_msg(record)
            self._build_extra(record)
            self._build_exception(record)
            fmt = self._sb.getvalue()
            return fmt

        return formatter

    def _build_level(self, record):
        self._sb.write(f"\"level\": ")
        if self._lever_formatter is not None:
            level = record["level"]
            self._sb.write(self._lever_formatter(level))
        else:
            self._sb.write("\"{level}\"")

    def _build_time(self):
        if self._display_time:
            self._sb.write(", ")
            self._sb.write(f"\"time\": \"{{time:{self._time_format}}}\"")

    def _build_elapsed(self, record):
        if self._display_elapsed:
            self._sb.write(", ")
            self._sb.write("\"elapsed\": ")
            if self._elapsed_formatter is not None:
                elapsed = record["elapsed"]
                self._sb.write(self._elapsed_formatter(elapsed))
            else:
                self._sb.write("\"{elapsed}\"")

    def _build_process(self, record):
        if self._display_process:
            self._sb.write(", ")
            self._sb.write("\"process\": ")
            if self._process_formatter is not None:
                process = record["process"]
                self._sb.write(self._process_formatter(process))
            else:
                self._sb.write("\"{process}\"")

    def _build_thread(self, record):
        if self._display_thread:
            self._sb.write(", ")
            self._sb.write("\"thread\": ")
            if self._thread_formatter is not None:
                thread = record["thread"]
                self._sb.write(self._thread_formatter(thread))
            else:
                self._sb.write("\"{thread}\"")

    def _build_file(self, record):
        if self._display_file:
            self._sb.write(", ")
            self._sb.write("\"file\": ")
            if self._file_formatter is not None:
                file = record["file"]
                self._sb.write(self._file_formatter(file))
            else:
                self._sb.write("\"{file}\"")

    def _build_line(self, record):
        if self._display_line:
            self._sb.write(", ")
            self._sb.write("\"line\": {line}")

    def _build_function(self, record):
        if self._display_function:
            self._sb.write(", ")
            self._sb.write("\"function\": \"{function}\"")

    def _build_module(self, record):
        if self._display_module:
            self._sb.write(", ")
            self._sb.write("\"module\": \"{module}\"")

    def _build_name(self, record):
        if self._display_name:
            self._sb.write(", ")
            self._sb.write("\"name\": \"{name}\"")

    def _build_msg(self, record):
        msg = record["message"]
        self._sb.write(", ")
        self._sb.write("\"msg\":")
        self._sb.write(escape_colorized(escape_format(json.dumps(msg, cls=CustomJSONEncoder, ensure_ascii=False))))

    def _build_extra(self, record):
        extra = record["extra"]
        if extra:
            self._sb.write(", ")
            self._sb.write("\"extra\":")
            self._sb.write(
                escape_colorized(escape_format(json.dumps(extra, cls=CustomJSONEncoder, ensure_ascii=False))))

    def _build_exception(self, record):
        exception = record["exception"]
        if exception is not None:
            self._sb.write("\n{exception}")
