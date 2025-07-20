# Contributing to Sparkie

Thank you for your interest in contributing to Sparkie! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/your-username/sparkie.git
cd sparkie
```

2. **Set up the development environment**
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment with Python 3.12+
uv venv --python 3.12
source .venv/bin/activate

# Install dependencies
uv sync --dev
```

3. **Install pre-commit hooks**
```bash
uv run pre-commit install
```

## Code Quality Standards

### Code Formatting
- Use **Ruff** for code formatting and linting
- Line length: 88 characters maximum
- Use double quotes for strings
- Follow PEP 8 naming conventions

### Type Hints
- Add type hints to all functions and methods
- Use modern Python 3.12+ type syntax (`dict` instead of `Dict`)
- Return type annotations are required

### Documentation
- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include type information in docstrings when helpful

### Testing
- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

## Development Workflow

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write code following the style guidelines
- Add tests for new functionality
- Update documentation as needed

3. **Run quality checks**
```bash
# Format code
uv run ruff format .

# Check for linting issues
uv run ruff check .

# Run type checking
uv run pyright

# Run tests
uv run pytest
```

4. **Commit your changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

5. **Push and create a pull request**
```bash
git push origin feature/your-feature-name
```

## Project Structure

- `0_⚡️_Welcome_to_Sparkie.py` - Main Streamlit application entry point
- `pages/` - Streamlit pages for different calculators
- `get_data.py` - Data fetching and processing utilities
- `params.py` - Configuration parameters and constants
- `tests/` - Test suite
- `*.csv` - Data files

## Commit Message Convention

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Issues and Feature Requests

- Use GitHub Issues to report bugs or request features
- Provide clear descriptions and reproduction steps for bugs
- Check existing issues before creating new ones

## Questions?

If you have questions about contributing, feel free to:
- Open a GitHub Discussion
- Create an issue with the `question` label
- Reach out to the maintainers