import enum
import sys
import time
from threading import Lock


class LogLevel(str, enum.Enum):
    trace = 'TRACE'
    info = 'INFO'
    warning = 'WARN'
    error = 'ERROR'


class RoboLogger(object):
    def __init__(self):
        self._entries = []

    def log(self, level: LogLevel, message: str):
        ts = time.time() * 1000
        self._entries.append(f'*{level}:{ts}* {message}')

    def flush(self) -> str:
        output = '\n'.join(self._entries)
        self._entries.clear()
        return output

    def __len__(self):
        return len(self._entries)


class SyncRoboLogger(RoboLogger):
    def __init__(self):
        super().__init__()
        self._mtx = Lock()

    def log(self, *args, **kwargs):
        with self._mtx:
            super().log(*args, **kwargs)

    def flush(self) -> str:
        with self._mtx:
            return super().flush()


class SyncLogStream(object):
    def __init__(self, logger: RoboLogger, level: LogLevel):
        self._logger = logger
        self._level = level
        self._line_buf = ''
        self._mutex = Lock()

    def write(self, s: str, /):
        line = None
        with self._mutex:
            if s.endswith('\n'):
                line = self._line_buf + s[:-1]
                self._line_buf = ''
            else:
                self._line_buf += s

        if line is not None:
            self._logger.log(self._level, line)


class StreamInterceptor(object):
    def __init__(self):
        self._logger = SyncRoboLogger()
        self._sys_out = None
        self._sys_err = None

    def __enter__(self):
        self._sys_out = sys.stdout
        self._sys_err = sys.stderr

        sys.stdout = SyncLogStream(self._logger, level=LogLevel.info)
        sys.stderr = SyncLogStream(self._logger, level=LogLevel.error)

        return self

    def __exit__(self, *exc_info):
        sys.stdout = self._sys_out
        sys.stderr = self._sys_err
        self.output = self._logger.flush()
