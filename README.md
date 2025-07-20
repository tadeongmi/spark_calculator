# Sparkie / Spark Calculator

Sparkie is a collection of tools to help users and developers experience Spark. 
Built by Phoenix Labs with data from BlockAnalitica.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (modern Python package manager)

## Installation Instructions

1. **Clone the repository**
```bash
git clone https://github.com/marsfoundation/sparkie.git
cd sparkie
```

2. **Set up Python environment**
```bash
# Install Python 3.12+ if needed
uv python install 3.12

# Create virtual environment
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
# Install project dependencies
uv sync

# Install development dependencies (optional)
uv sync --dev
```

4. **Run the application**
```bash
streamlit run "0_⚡️_Welcome_to_Sparkie.py"
```

The app will be available at `http://localhost:8501`

## Development

### Code Quality Tools

The project includes several development tools:

- **Ruff**: Code formatting and linting
- **Pyright**: Type checking
- **Pre-commit**: Git hooks for code quality

```bash
# Format code
uv run ruff format .

# Check code quality
uv run ruff check .

# Type checking
uv run pyright

# Install pre-commit hooks
uv run pre-commit install
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov
```

### Project Structure

```
spark_calculator/
├── 0_⚡️_Welcome_to_Sparkie.py    # Main Streamlit app
├── pages/                        # Streamlit pages
│   ├── 1_🏦_SparkLend.py        # SparkLend calculator
│   └── 2_💸_sDAI.py             # sDAI calculator  
├── get_data.py                   # Data fetching utilities
├── params.py                     # Configuration parameters
├── tests/                        # Test suite
├── data files (*.csv)            # Data sources
└── pyproject.toml               # Project configuration
```