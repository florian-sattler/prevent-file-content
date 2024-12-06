import argparse
import enum
import pathlib
import re
import typing


class Status(enum.Enum):
    SUCCESS = enum.auto()
    FILE_READ_ERROR = enum.auto()
    PATTERN_FOUND = enum.auto()


def is_pattern_present_in_file(file_content: str, regex: re.Pattern) -> bool:
    return regex.search(file_content) is not None


def validate_paths(paths: typing.Any) -> list[pathlib.Path]:
    if not isinstance(paths, list):
        raise ValueError("Paths must be a list")

    result: list[pathlib.Path] = []
    for path in paths:
        if not isinstance(path, pathlib.Path):
            raise ValueError("Path must be a pathlib.Path object")

        if not path.exists():
            raise FileNotFoundError(f"Path {path} does not exist")

        if not path.is_file():
            raise ValueError(f"Path {path} is not a file")

        result.append(path)

    return result


def validate_patterns(patterns: typing.Any) -> list[re.Pattern]:
    if not isinstance(patterns, list):
        raise ValueError("Patterns must be a list")

    result: list[re.Pattern] = []
    for pattern in patterns:
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string")

        try:
            result.append(re.compile(pattern))
        except re.error as e:
            raise ValueError(f"Pattern {pattern} is not a valid regex: {e}")

    return result


def process_file(path: pathlib.Path, patterns: list[re.Pattern]) -> Status:
    if path.name == ".pre-commit-config.yaml":
        return Status.SUCCESS

    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return Status.FILE_READ_ERROR

    for pattern in patterns:
        if is_pattern_present_in_file(text, pattern):
            return Status.PATTERN_FOUND

    return Status.SUCCESS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=pathlib.Path,
        nargs="+",
        help="Files to check for forbidden patterns",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        action="append",
        help="Pattern to prevent in files, can be specified multiple times",
    )
    args = parser.parse_args()

    try:
        paths = validate_paths(args.filename)
    except (ValueError, FileNotFoundError) as e:
        print(e)
        return

    try:
        patterns = validate_patterns(args.pattern)
    except ValueError as e:
        print(e)
        return

    error: bool = False
    for path in paths:
        status = process_file(path, patterns)
        match status:
            case Status.SUCCESS:
                print(f"{path} ok")
            case Status.FILE_READ_ERROR:
                print(f"{path} could not be read")
                error = True
            case Status.PATTERN_FOUND:
                print(f"{path} contains forbidden pattern")
                error = True

    if error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
