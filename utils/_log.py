# coding=utf-8
# Powered by SoaringNova Technology Company
import datetime
import sys


def format_print():
    class GeneralWriter:
        def __init__(self, *writers):
            self.writers = writers

        def write(self, buf):
            now = datetime.datetime.now()
            ts = f"{now.strftime('%Y-%m-%d %H:%M:%S')},{'%03d' % (now.microsecond // 1000)}"
            for w in self.writers:
                for line in buf.rstrip().splitlines():
                    msg = line.rstrip()
                    if len(msg):
                        w.write(f'\033[1;32;1m{ts}| {msg}\033[0m\n')

        def flush(self):
            pass

        def isatty(self):
            return any(writer.isatty() for writer in self.writers)

    sys.stdout = GeneralWriter(sys.stdout)
    sys.stderr = GeneralWriter(sys.stdout)
