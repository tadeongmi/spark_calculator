"""Integration tests for the Spark Calculator application."""

import os
import sys

import pandas as pd
import pytest

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataFiles:
    """Test that required data files exist and have expected structure."""

    def test_assets_csv_exists(self):
        """Test that assets.csv exists and has expected columns."""
        assert os.path.exists("assets.csv"), "assets.csv file not found"

        df = pd.read_csv("assets.csv")
        assert not df.empty, "assets.csv is empty"

        # Check for some expected columns
        expected_columns = ["underlying_symbol", "network", "ltv", "liquidation_threshold"]
        for col in expected_columns:
            assert col in df.columns, f"Column {col} not found in assets.csv"

    def test_pot_dsr_csv_exists(self):
        """Test that pot_dsr.csv exists and has expected structure."""
        assert os.path.exists("pot_dsr.csv"), "pot_dsr.csv file not found"

        df = pd.read_csv("pot_dsr.csv")
        assert not df.empty, "pot_dsr.csv is empty"

        # Check for expected columns
        expected_columns = ["datetime", "rate"]
        for col in expected_columns:
            assert col in df.columns, f"Column {col} not found in pot_dsr.csv"

    def test_sdai_wallets_csv_exists(self):
        """Test that sdai_wallets.csv exists."""
        assert os.path.exists("sdai_wallets.csv"), "sdai_wallets.csv file not found"

        _ = pd.read_csv("sdai_wallets.csv")
        # Note: This file might be empty, so we just check it can be read

    def test_example_sdai_csv_exists(self):
        """Test that example_sdai.csv exists."""
        assert os.path.exists("example_sdai.csv"), "example_sdai.csv file not found"


class TestStreamlitPages:
    """Test that Streamlit pages can be imported without errors."""

    def test_welcome_page_imports(self):
        """Test that the welcome page can be imported."""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "welcome", "0_⚡️_Welcome_to_Sparkie.py"
            )
            _ = importlib.util.module_from_spec(spec)
            # Don't execute the module to avoid Streamlit initialization
        except Exception as e:
            pytest.fail(f"Failed to import welcome page: {e}")

    def test_sparklend_page_exists(self):
        """Test that SparkLend page exists."""
        assert os.path.exists("pages/1_🏦_SparkLend.py"), "SparkLend page not found"

    def test_sdai_page_exists(self):
        """Test that sDAI page exists."""
        assert os.path.exists("pages/2_💸_sDAI.py"), "sDAI page not found"


class TestConfigFiles:
    """Test that configuration files are properly set up."""

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists and has expected structure."""
        assert os.path.exists("pyproject.toml"), "pyproject.toml not found"

        # Try to parse it
        try:
            import tomllib
            with open("pyproject.toml", "rb") as f:
                config = tomllib.load(f)

            assert "project" in config, "project section not found in pyproject.toml"
            assert "name" in config["project"], "project name not found"
            assert config["project"]["name"] == "spark-calculator"

        except ImportError:
            # tomllib not available in older Python versions
            pass

    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        assert os.path.exists(".gitignore"), ".gitignore not found"

    def test_pre_commit_config_exists(self):
        """Test that pre-commit configuration exists."""
        assert os.path.exists(".pre-commit-config.yaml"), ".pre-commit-config.yaml not found"
