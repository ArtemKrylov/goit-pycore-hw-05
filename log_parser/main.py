import sys
from typing import Literal, Optional, TypedDict, get_args

from colorama import Fore, just_fix_windows_console

from decorators import handle_file_errors, input_error

LogLevel = Literal["INFO", "ERROR", "DEBUG", "WARNING"]


LOG_LEVELS = get_args(LogLevel)


class LevelStats(TypedDict):
    length: int
    logs: list[dict[str, str]]


def parse_log_line(line: str) -> Optional[dict[str, str]]:
    """Parse a log entry, returning None for a blank line."""
    if not line or not line.strip():
        return None

    date, time, level, message = line.split(maxsplit=3)

    return {"date": date, "time": time, "level": level, "message": message}


@handle_file_errors
def load_logs(file_path: str) -> list[dict[str, str]]:
    """Load log entries from a UTF-8 file."""
    if not file_path:
        print("No file path")
        raise ValueError("No file path")

    logs = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            log = parse_log_line(line.strip())
            if log:
                logs.append(log)
    return logs


@input_error
def filter_logs_by_level(
    logs: list[dict[str, str]], level: LogLevel | None = None
) -> list[dict[str, str]]:
    """Filter log entries by level, ignoring case."""
    if not logs:
        return []
    if not level:
        return logs

    return list(filter(lambda log: log["level"].casefold() == level.casefold(), logs))


def count_logs_by_level(logs: list[dict[str, str]]) -> dict[str, LevelStats]:
    """Group log entries by level and count them."""
    result = {}
    for level in LOG_LEVELS:
        level_logs = filter_logs_by_level(logs, level)
        result[level] = {"length": len(level_logs), "logs": level_logs}
    return result


@input_error
def display_log_counts(counts: dict[str, LevelStats], level: LogLevel | None = None):
    """Print log counts and optional details for a selected level."""
    sorted_counts = dict(
        sorted(counts.items(), key=lambda item: item[1]["length"], reverse=True)
    )
    logs_to_display = "\n".join(
        f"{Fore.BLUE if level and count_level.casefold()==level.casefold() else ''}{count_level:<16}{Fore.RESET} | {count['length']}"
        for count_level, count in sorted_counts.items()
    )
    log_level_title = f"Деталі логів для рівня {level.upper()}:\n" if level else ""
    log_level_detailes = (
        "\n".join([" ".join(log.values()) for log in counts[level.upper()]["logs"]])
        if level
        else ""
    )

    print(f"""\nРівень логування | Кількість
-----------------|----------
{logs_to_display}

{log_level_title}{log_level_detailes}
""")


if __name__ == "__main__":
    just_fix_windows_console()
    if len(sys.argv) <= 1:
        print("No log file path")
        sys.exit(1)
    path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None
    all_logs = load_logs(path)
    logs = count_logs_by_level(all_logs)
    display_log_counts(logs, level)
