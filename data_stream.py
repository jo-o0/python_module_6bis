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
    print(" * * * DATA STREAM * * * ")
    print("\nInitialize data Stream...")
    stream: DataStream = DataStream()
    stream.print_processors_stats()
    numeric: NumericProcessor = NumericProcessor()
    print("\nRegistering Numeric Processor...")
    stream.register_processor(numeric)
    batch: list[Any] = [
        'Hello World',
        [3.14, -1, 2.71],
        [{'log_level': 'WARNING', 'log_message': 'Telnet access!'},
         {'log_level': 'INFO', 'log_message': 'User connected'}],
        42,
        ['Hi', 'five']
    ]
    print(f"\nSending first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    text: TextProcessor = TextProcessor()
    logs: LogProcessor = LogProcessor()
    print("\nRegistering other data processors")
    stream.register_processor(text)
    stream.register_processor(logs)
    print(f"\nSend the same batch again: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print("\nConsume some elements: Numeric 3, Text 2, Log 1")
    print("\n=== DATA STREAM STATS ===")
    stream.print_processors_stats()


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

    @property
    def pending(self) -> int:
        return len(self._stored)

    def output(self) -> tuple[int, str]:
        if not self._stored:
            raise EmptyBufferError("Erm... The buffer is empty...\n"
                                   "Nothing to do here... :/")
        item: tuple[int, str] = self._stored.pop(0)
        return item


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._totals: dict[str, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._totals[type(proc).__name__] = 0

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            routed: bool = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    count: int = (len(element)
                                  if isinstance(element, list) else 1)
                    self._totals[type(proc).__name__] += count
                    routed = True
                    break
            if not routed:
                print(f"\nDataStream error: Can't process element in stream :/"
                      f"\n{element}")

    def print_processors_stats(self) -> None:
        if not self._processors:
            print("No processors nor data found :/")
            return
        for proc in self._processors:
            name: str = type(proc).__name__
            total: int = self._totals[name]
            remaining: int = proc.pending
            print(f"\n{name}: total {total} items processed,"
                  f" remaining {remaining} on processor")


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        items: list[Any] = [data] if not isinstance(data, list) else data
        try:
            converted: list[float] = [float(elem) for elem in items]
        except (ValueError, TypeError):
            return False
        if not all(value == value for value in converted):
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
                f"Improper Numeric Data\n"
                f"* Caught some non-numeric data 0o0:\n {rejected}"
            )


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        items: list[Any] = [data] if not isinstance(data, list) else data
        return all(isinstance(elem, str) for elem in items)

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
        items: list[Any] = [data] if not isinstance(data, list) else data
        return all(isinstance(elem, dict)
                   and 'log_level' in elem
                   and 'log_message' in elem
                   and all(isinstance(val, str) for val in elem.values())
                   for elem in items)

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


if __name__ == "__main__":
    main()
