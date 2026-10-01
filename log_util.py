# log_util.py
# Homemade logger for KM-Waechter.

import time

LOG_LINES: list[str] = []
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped entry to the in-memory log buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to the given file, then clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
