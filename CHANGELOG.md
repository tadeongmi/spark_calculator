# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-07-21

### Changed
- **BREAKING**: Migrated from Poetry to uv package management
- **BREAKING**: Updated Python requirement to 3.12+
- Updated all dependencies to latest versions:
  - pandas: 2.1.4 → 2.3.1
  - streamlit: 1.29.0 → 1.47.0
  - watchdog: 3.0.0 → 6.0.0

### Added
- Development tools and quality infrastructure:
  - Ruff for code formatting and linting
  - Pyright for type checking
  - Pre-commit hooks for automated quality checks
  - pytest test suite with coverage reporting
- Type hints throughout codebase
- Docstrings for public functions
- Comprehensive test suite with 16 test cases
- Modern Python 3.12 syntax support
- `.gitignore` file for better repository hygiene
- `CONTRIBUTING.md` with development guidelines
- Updated `README.md` with new installation instructions

### Fixed
- Implemented missing `get_data()` function with proper error handling
- Replaced bare `except:` statements with specific exception types
- Fixed boolean comparison issues (`== True/False` → proper boolean checks)
- Fixed comparison issues (`== None` → `is None`)
- Resolved all code quality issues identified by Ruff
- Added proper path handling for data files
- Fixed division by zero warnings in calculation functions

### Improved
- Code quality and maintainability
- Error handling and validation
- Development workflow with automated tools
- Documentation and setup instructions
- Project structure and organization

## [0.1.0] - 2024-01-XX

### Added
- Initial release
- SparkLend Calculator for health factors and liquidation calculations
- sDAI Calculator for yield calculations
- Streamlit web interface
- Basic data processing from CSV files
- Integration with BlockAnalitica data