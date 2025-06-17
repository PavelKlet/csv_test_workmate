import os
import pytest
from data_operations import Filter, Aggregator, Sorter, CSVProcessor

FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "products.csv")

@pytest.fixture
def processor():
    return CSVProcessor(FILE_PATH, filterer=Filter(), aggregator=Aggregator(), sorter=Sorter())

def test_filter_by_brand(processor):
    processor.filter("brand", "eq", "apple")
    assert all(row["brand"] == "apple" for row in processor.rows)
    assert len(processor.rows) == 4

def test_aggregate_avg_price(processor):
    avg_price = processor.aggregator.avg([float(row["price"]) for row in processor._read_csv()])
    assert pytest.approx(avg_price) == pytest.approx(
        (999 + 1199 + 199 + 799 + 349 + 299 + 429 + 999 + 149 + 599) / 10
    )

def test_aggregate_min_price(processor):
    processor.aggregate("price", "min")
    assert len(processor.rows) == 1
    assert processor.rows[0]["price"] == "149"
    assert processor.rows[0]["name"] == "redmi 10c"

def test_sort_by_rating_desc(processor):
    processor.order_by("rating", "desc")
    ratings = [float(row["rating"]) for row in processor.rows]
    assert ratings == sorted(ratings, reverse=True)
    assert processor.rows[0]["name"] == "iphone 15 pro"

def test_full_pipeline(processor):
    processor.filter("brand", "eq", "samsung")
    processor.order_by("price", "asc")
    processor.aggregate("rating", "min")
    assert all(row["brand"] == "samsung" for row in processor.rows)
    assert len(processor.rows) == 1
    assert processor.rows[0]["rating"] == "4.2"
    assert processor.rows[0]["name"] == "galaxy a54"

def test_invalid_filter_operator(processor):
    with pytest.raises(ValueError, match="Unsupported operator: neq"):
        processor.filter("brand", "neq", "apple")

def test_invalid_aggregate_type(processor):
    with pytest.raises(ValueError, match="Unsupported aggregation type: median"):
        processor.aggregate("price", "median")

def test_invalid_sort_order(processor):
    with pytest.raises(ValueError):
        processor.order_by("rating", "upward")

def test_empty_data_filter():
    processor = CSVProcessor(FILE_PATH, filterer=Filter())
    processor.rows = []
    processor.filter("brand", "eq", "apple")
    assert processor.rows == []

def test_empty_data_aggregate():
    processor = CSVProcessor(FILE_PATH, aggregator=Aggregator())
    processor.rows = []
    with pytest.raises(ZeroDivisionError):
        processor.aggregate("price", "avg")

def test_missing_column_in_filter():
    processor = CSVProcessor(FILE_PATH)
    with pytest.raises(RuntimeError):
        processor.filter("nonexistent_column", "eq", "value")

def test_pipeline_complex_case(processor):
    processor.filter("brand", "eq", "xiaomi")
    processor.order_by("price", "asc")
    processor.aggregate("rating", "max")
    assert len(processor.rows) == 1
    assert processor.rows[0]["name"] == "redmi note 12"

def test_immutability_of_original_data(processor):
    original_rows = processor._read_csv()
    processor.filter("brand", "eq", "apple")
    processor.order_by("price", "asc")
    assert processor._read_csv() == original_rows
