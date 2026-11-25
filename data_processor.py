from typing import Any
from abc import ABC, abstractmethod


class ImproperNumericDataError(Exception):
    ...


class ImproperTextDataError(Exception):
    ...


class ImproperLogDataError(Exception):
    ...


class EmptyBufferError(Exception):
    ...


def main() -> None:
    print(" * * * DATA PROCESSOR * * * ")
    test_numeric()
    test_text()
    test_log()


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._stored: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        if not self._stored:
            raise EmptyBufferError("Erm... The buffer is empty...\n"
                                   "Nothing to do here... :/")
        item: tuple[int, str] = self._stored.pop(0)
        return item


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            value: float = float(data)
        except (ValueError, TypeError):
            return False
        if value != value:
            return False
        return True

    def ingest(self, data: int | float | list[int | float]) -> None:
        items: list[int | float]
        items = [data] if not isinstance(data, list) else data
        converted: list[float] = []
        rejected: list[Any] = []
        for elem in items:
            try:
                converted.append(float(elem))
            except (ValueError, TypeError):
                rejected.append(elem)
        for value in converted:
            text: str = str(int(value)) if value.is_integer() else str(value)
            self._stored.append((self._rank, text))
            self._rank += 1
        if rejected:
            raise ImproperNumericDataError(
                f"Improper Numeric Data\n*"
                f"Caught some non-numeric data 0o0:\n {rejected}"
            )


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        items: list[str]
        items = [data] if not isinstance(data, list) else data
        passed: list[str] = []
        rejected: list[Any] = []
        for elem in items:
            if isinstance(elem, str):
                passed.append(elem)
            else:
                rejected.append(elem)
        for value in passed:
            self._stored.append((self._rank, value))
            self._rank += 1
        if rejected:
            raise ImproperTextDataError(
                f"Improper Text Data\n"
                f"*Caught some non-text data 0o0:\n {rejected}"
            )


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if not isinstance(data, dict):
            return False
        if 'log_level' not in data or 'log_message' not in data:
            return False
        return all(isinstance(elem, str) for elem in data.values())

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        items: list[dict[str, str]]
        items = [data] if not isinstance(data, list) else data
        passed: list[str] = []
        rejected: list[Any] = []
        for elem in items:
            if (isinstance(elem, dict)
                and 'log_level' in elem
                    and 'log_message' in elem
                        and all(isinstance(v, str) for v in elem.values())):
                formatted: str = (
                    f"{elem['log_level']}: {elem['log_message']}")
                passed.append(formatted)
            else:
                rejected.append(elem)
        for value in passed:
            self._stored.append((self._rank, value))
            self._rank += 1
        if rejected:
            raise ImproperLogDataError(
                f"Improper Log Data\nCaught non-log data 0o0:\n{rejected}"
            )


def test_numeric() -> None:
    numeric: NumericProcessor = NumericProcessor()
    print("\n* TESTING NUMERIC PROCESSOR...")
    print(f"\nTrying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except ImproperNumericDataError as e:
        print(f"\nGot an Exception: {e}")
    print("\nProcessing Data: 1, 2, 3, 4, 5")
    trial_list: list = [1, 2, 3, 4, 5]
    numeric.ingest(trial_list)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Nunmeric value {rank}: {value}")


def test_text() -> None:
    print("\n* TESTING TEXT PROCESSOR...")
    text: TextProcessor = TextProcessor()
    print(f"\nTrying to validate input '42': {text.validate(42)}")
    print(f"Trying to validate input 'Hello': {text.validate('Hello')}")
    print("\nProcessing Data: 'Hello', 'Nexus', 'World'")
    trial_list: list = ["Hello", "Nexus", "World"]
    text.ingest(trial_list)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")


def test_log() -> None:
    log: LogProcessor = LogProcessor()
    data: list[dict[str, str]] = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    print("\n* TESTING LOG PROCESSOR...")
    print(f"\nTrying to validate input 'Hello': {log.validate('Hello')}")
    print(f"\nProccesing data:\n {data}")
    log.ingest(data)
    print("\nExtracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log {rank}: {value}")


if __name__ == "__main__":
    main()
