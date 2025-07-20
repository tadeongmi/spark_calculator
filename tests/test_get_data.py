"""Tests for the get_data module."""

import os
import sys
from unittest.mock import patch

import pandas as pd
import pytest

# Add the parent directory to the path to import get_data
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from get_data import get_data


class TestGetData:
    """Test cases for the get_data function."""

    def test_get_data_unknown_source(self):
        """Test that get_data raises ValueError for unknown data source."""
        with pytest.raises(ValueError, match="Unknown data source"):
            get_data("invalid_source")

    def test_get_data_valid_sources(self):
        """Test that get_data accepts all known data sources."""
        valid_sources = [
            "spark_v1ethereummarket",
            "spark_v1gnosismarket",
            "spark_v1ethereumemodecategoryaddedevent",
            "spark_v1ethereumsdaimarket",
            "spark_v1potdsr",
            "spark_v1ethereumcurrentmarketstate"
        ]

        # Mock pd.read_csv to return a dummy DataFrame
        mock_df = pd.DataFrame({"test": [1, 2, 3], "network": ["ethereum", "gnosis", "ethereum"]})

        with patch('pandas.read_csv', return_value=mock_df):
            for source in valid_sources:
                result = get_data(source)
                assert isinstance(result, pd.DataFrame)

    def test_get_data_file_not_found(self):
        """Test that get_data raises FileNotFoundError when CSV file doesn't exist."""
        with patch('pandas.read_csv', side_effect=FileNotFoundError("File not found")):
            with pytest.raises(FileNotFoundError, match="Required data file not found"):
                get_data("spark_v1ethereummarket")

    def test_get_data_empty_file(self):
        """Test that get_data raises ValueError for empty CSV files."""
        with patch('pandas.read_csv', side_effect=pd.errors.EmptyDataError("Empty file")):
            with pytest.raises(ValueError, match="Data file is empty"):
                get_data("spark_v1ethereummarket")

    def test_get_data_network_filtering(self):
        """Test that get_data correctly filters by network."""
        # Create mock DataFrame with network column
        mock_df = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "network": ["ethereum", "gnosis", "ethereum", "gnosis"],
            "symbol": ["ETH", "GNO", "DAI", "XDAI"]
        })

        with patch('pandas.read_csv', return_value=mock_df):
            # Test ethereum filtering
            eth_result = get_data("spark_v1ethereummarket")
            assert len(eth_result) == 2
            assert all(eth_result["network"] == "ethereum")

            # Test gnosis filtering
            gnosis_result = get_data("spark_v1gnosismarket")
            assert len(gnosis_result) == 2
            assert all(gnosis_result["network"] == "gnosis")

    def test_get_data_no_network_column(self):
        """Test that get_data works when network column doesn't exist."""
        # Create mock DataFrame without network column
        mock_df = pd.DataFrame({
            "id": [1, 2, 3],
            "symbol": ["ETH", "DAI", "USDC"]
        })

        with patch('pandas.read_csv', return_value=mock_df):
            result = get_data("spark_v1ethereummarket")
            assert len(result) == 3
            assert "network" not in result.columns
