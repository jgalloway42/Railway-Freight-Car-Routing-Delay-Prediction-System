# Code Style and Conventions

## Import Style
- **Explicit imports**: No `import *` statements
- **Grouped imports**: Organized by purpose (core libraries, data management, paths)
- **Standard pattern** (from template notebook):
  ```python
  # Core data science libraries
  from generic.preamble import np, pd, plt, sns
  # Data management and paths
  from generic.preamble import raw_data, processed_data, models_path
  from generic.helpers import create_data_catalog
  ```

## Naming Conventions
- **Variables/functions**: snake_case
- **Classes**: PascalCase (e.g., DataCatalog)
- **Files**: Descriptive lowercase with underscores, no spaces or special characters
- **Notebooks**: Prefix with "zz_" for templates

## File Organization
- **Raw data**: Store in `data/raw/` (never modify)
- **Cleaned data**: Place in `data/processed/`
- **Intermediate data**: Use `data/interim/` for processing steps
- **Models**: Save in `models/` directory
- **Figures**: Generate in `reports/figures/`
- **Scripts**: Keep in `scripts/` directory

## Path Handling
- Use pathlib for cross-platform compatibility
- All paths use forward slashes or pathlib.Path objects
- Import predefined paths from preamble.py (project_root, raw_data, etc.)

## Windows Compatibility
- Avoid Unicode characters in file names and code comments
- Use UTF-8 encoding for text files:
  ```python
  df.to_csv('file.csv', encoding='utf-8')
  pd.read_csv('file.csv', encoding='utf-8')
  ```
- Pathlib used throughout for robust Windows support

## Data Access Pattern
- Use DataCatalog for file discovery and loading
- Example workflow:
  ```python
  catalog = create_data_catalog('.')
  df = catalog.load_file('filename')
  path = catalog.get_path('filename')
  files = catalog.find_files('pattern')
  ```

## Documentation
- Comprehensive documentation in `docs/` directory
- README.md for project overview
- QUICKSTART.md for fast setup
- CLAUDE.md for AI assistant guidance
- Detailed guides in docs/ for advanced topics