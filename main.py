import argparse

from data_operations import Filter, Aggregator, Sorter, CSVProcessor


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process a CSV file with filtering and aggregation."
    )
    parser.add_argument("file", type=str, help="Path to the CSV file")
    parser.add_argument(
        "--filter",
        nargs=3,
        metavar=("COLUMN", "OPERATOR", "VALUE"),
        help="Filter rows (operators: eq, lt, gt)",
    )
    parser.add_argument(
        "--aggregate",
        nargs=2,
        metavar=("COLUMN", "AGG_TYPE"),
        help="Aggregate a column (types: avg, min, max)",
    )
    parser.add_argument(
        "--order-by",
        nargs=2,
        metavar=("COLUMN", "ORDER"),
        help="Order rows by a column (order: asc, desc)",
    )

    args = parser.parse_args()

    filterer = Filter() if args.filter else None
    aggregator = Aggregator() if args.aggregate else None
    sorter = Sorter() if args.order_by else None

    processor = CSVProcessor(args.file, filterer, aggregator, sorter)

    if args.filter:
        col, op, val = args.filter
        processor.filter(col, op, val)

    if args.aggregate:
        col, agg = args.aggregate
        processor.aggregate(col, agg)

    if args.order_by:
        col, order = args.order_by
        processor.order_by(col, order)

    print("\nProcessed rows:")
    processor.display()


if __name__ == "__main__":
    main()
