# Codebase Structure

## Directory Layout

```
Railway-Freight-Car-Routing-Delay-Prediction-System/
├── src/                    # Source code (all directories have __init__.py)
│   ├── generic/           # Core utilities shared across project
│   │   ├── preamble.py   # Standard imports, configs, path management
│   │   └── helpers.py    # DataCatalog and utility functions
│   ├── data_prep/        # Data preparation and cleaning modules
│   ├── features/         # Feature engineering modules
│   ├── models/           # Model training and evaluation modules
│   └── visualization/    # Custom plotting functions
├── data/                  # Data storage (created by setup script)
│   ├── raw/              # Original, immutable data
│   ├── processed/        # Final datasets for modeling
│   ├── interim/          # Intermediate transformed data
│   └── external/         # Third-party data sources
├── notebooks/            # Jupyter notebooks for analysis
│   └── zz_template_notebook.ipynb  # Pre-configured template
├── models/               # Trained models and artifacts (Python package)
├── reports/figures/      # Generated visualizations
├── scripts/              # Setup and utility scripts
│   └── env-setup.sh     # Automated environment setup
├── docs/                 # Documentation
│   ├── CLAUDE.md        # AI assistant guide
│   ├── setup.md         # Detailed setup guide
│   ├── data-workflow.md # DataCatalog usage guide
│   └── notebook-guide.md # Development best practices
├── .mcp.json            # Serena MCP server configuration
└── requirements.txt     # Python dependencies
```

## Key Modules

### src/generic/preamble.py
- Exports: np, pd, plt, sns (standard data science imports)
- Exports: project_root, raw_data, processed_data, interim_data, external_data, models_path, figures_path
- Robust path management using pathlib
- Cross-platform compatibility (Windows/Linux)

### src/generic/helpers.py
Main symbols:
- `DataCatalog` (class): File discovery and data loading system
- `create_data_catalog()`: Factory function for DataCatalog
- `walk_directory()`: Directory traversal utility
- `search_columns()`, `filter_list()`, `flatten_list()`: Data manipulation
- `plot_df()`, `plotly_graph()`: Visualization with caching
- `save_joblib()`: Model persistence
- `get_logger()`: Logging setup

## Package Structure
All directories in src/ are proper Python packages with __init__.py files for clean imports.