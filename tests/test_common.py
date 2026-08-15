import sys
sys.path.append('../src')

from unittest.mock import patch, MagicMock
from common import table_has_data
from common import extract_data
from common import load_data
from sqlalchemy.exc import ProgrammingError
import pandas as pd
import polars as pl


def test_table_has_data_returns_true_when_rows_exist():
    mock_engine = MagicMock()
    mock_conn = mock_engine.connect.return_value.__enter__.return_value
    mock_conn.execute.return_value.scalar.return_value = 5

    result = table_has_data(mock_engine, "some_table")

    assert result == True

def test_table_has_data_returns_false_when_no_rows():
    mock_engine = MagicMock()
    mock_conn = mock_engine.connect.return_value.__enter__.return_value
    mock_conn.execute.return_value.scalar.return_value = 0

    result = table_has_data(mock_engine, "some_table")

    assert result == False    

def test_table_has_data_returns_false_when_table_does_not_exist():
    mock_engine = MagicMock()
    mock_conn = mock_engine.connect.return_value.__enter__.return_value
    mock_conn.execute.side_effect = ProgrammingError("statement", "params", "orig")

    result = table_has_data(mock_engine, "nonexistent_table")

    assert result == False    


def test_extract_data_returns_polars_dataframe():
    fake_result = MagicMock()
    fake_result.write.return_value = pd.DataFrame({"country": ["Germany"], "value": [100]})

    with patch("common.pyjstat.Dataset.read", return_value=fake_result):
        df = extract_data("http://fake-url.com")

    assert isinstance(df, pl.DataFrame)
    assert df.shape[0] == 1    


def test_load_data_calls_write_database_correctly():
    mock_engine = MagicMock()
    mock_conn = mock_engine.begin.return_value.__enter__.return_value
    mock_df = MagicMock()

    load_data(mock_engine, "some_table", mock_df)

    mock_df.write_database.assert_called_once_with(
        table_name="some_table",
        connection=mock_conn,
        if_table_exists="fail"
    )    