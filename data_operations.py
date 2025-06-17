import csv

from tabulate import tabulate

class Filter:
    @staticmethod
    def eq(x: str, y: str) -> bool:
        return x == y

    @staticmethod
    def lt(x: str, y: str) -> bool:
        try:
            return float(x) < float(y)
        except ValueError:
            return x < y

    @staticmethod
    def gt(x: str, y: str) -> bool:
        try:
            return float(x) > float(y)
        except ValueError:
            return x > y

    methods = {
        "eq": eq,
        "lt": lt,
        "gt": gt,
    }

    def filter(self, rows: list[dict], column: str, operator: str, value: str) -> list[dict]:
        if operator not in self.methods:
            raise ValueError(f"Unsupported operator: {operator}")
        op_func = self.methods[operator]
        return [row for row in rows if op_func(row[column], value)]


class Aggregator:
    @staticmethod
    def avg(values: list[float]) -> float:
        return sum(values) / len(values)

    @staticmethod
    def min(values: list[float]) -> float:
        return min(values)

    @staticmethod
    def max(values: list[float]) -> float:
        return max(values)

    methods = {
        "avg": avg,
        "min": min,
        "max": max,
    }

    def aggregate(self, rows: list[dict], column: str, agg_type: str) -> list[dict]:
        values = [float(row[column]) for row in rows]
        if agg_type not in self.methods:
            raise ValueError(f"Unsupported aggregation type: {agg_type}")
        target_value = self.methods[agg_type](values)
        if agg_type == "avg":
            return target_value
        return [row for row in rows if float(row[column]) == target_value]

class Sorter:
    @staticmethod
    def order_by(rows: list[dict], column: str, order: str) -> list[dict]:

        if order not in {"asc", "desc"}:
            raise ValueError(f"Unsupported sort order: {order}")

        reverse = order == "desc"
        return sorted(rows,
                      key=lambda row: float(
                          row[column]) if row[column
                      ].replace('.', '', 1).isdigit() else row[column],
                      reverse=reverse)

class CSVProcessor:
    def __init__(
        self,
        file_path: str,
        filterer: Filter | None = None,
        aggregator: Aggregator | None = None,
        sorter: Sorter | None = None
    ) -> None:
        self.file_path = file_path
        self.rows = self._read_csv()
        self.filterer = filterer
        self.aggregator = aggregator
        self.sorter = sorter

    def _read_csv(self) -> list[dict]:
        with open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def filter(self, column: str, operator: str, value: str) -> None:
        if not self.filterer:
            raise RuntimeError("Filter functionality is not enabled")
        self.rows = self.filterer.filter(self.rows, column, operator, value)

    def aggregate(self, column: str, agg_type: str) -> None:
        if not self.aggregator:
            raise RuntimeError("Aggregation functionality is not enabled")
        result = self.aggregator.aggregate(self.rows, column, agg_type)
        if isinstance(result, list):
            self.rows = result
        else:
            print(f"\033[92mAggregation result ({agg_type}) for column '{column}': {result}\033[0m")

    def order_by(self, column: str, order: str) -> None:
        if not self.sorter:
            raise RuntimeError("Sorting functionality is not enabled")
        self.rows = self.sorter.order_by(self.rows, column, order)

    def display(self) -> None:
        print(tabulate(self.rows, headers="keys", tablefmt="grid"))