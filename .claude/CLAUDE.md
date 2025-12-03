# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working with this railway optimization repository.

## Project Overview

Railway Freight Car Routing & Delay Prediction System - combines MILP optimization (Pyomo/GLPK) with machine learning for routing and delay prediction. Built on a professional data science template framework. The goal is to learn OR and implement projects suitable for display to potential employers. The student has a background in chemical process engineering and applied mathematics at the graduate level. They have been working in continuous process optimiztion and needs to review/upgrade OR subject matter.

**Key Components:**
- **Optimization Engine** (`src/optimization/`): MILP-based routing using Pyomo
- **ML Pipeline** (`src/models/`): Delay prediction models
- **Data Management**: DataCatalog system for file discovery and loading
- **Framework**: Cookiecutter-data-science structure with enhanced utilities

## Quick Reference

### Project Structure
```
├── src/
│   ├── optimization/     # Railway routing MILP models (Pyomo)
│   ├── generic/          # DataCatalog, helpers, preamble
│   ├── data_prep/        # Data preparation modules
│   ├── features/         # Feature engineering
│   ├── models/           # ML models (delay prediction)
│   └── visualization/    # Custom plotting
├── data/                 # raw/, processed/, interim/
├── notebooks/            # Jupyter analysis notebooks
├── docs/                 # Comprehensive documentation
│   ├── railway-optimization.md  # MILP theory & implementation
│   ├── setup.md          # Environment setup
│   ├── data-workflow.md  # DataCatalog usage
│   └── notebook-guide.md # Notebook best practices
└── scripts/              # env-setup.sh
```

For detailed structure, see [docs/README.md](README.md).

### Key Files
- **Optimization examples**: `src/optimization/{assignment_example, railway_routing_simple, dataset_preparation}.py`
- **Theory guide**: `docs/railway-optimization.md` - MILP fundamentals, network flows, Pyomo
- **DataCatalog**: `src/generic/helpers.py` - File discovery and loading system
- **Preamble**: `src/generic/preamble.py` - Standard imports and path management

## Railway Optimization Specifics

### Optimization Models (`src/optimization/`)
- **assignment_example.py**: Simple worker-task assignment (MILP basics)
- **railway_routing_simple.py**: Multi-commodity flow on 4-node network
- **dataset_preparation.py**: Generate synthetic railway datasets

### Theory & Implementation
See `docs/railway-optimization.md` for:
- MILP formulation and canonical forms
- Network flow problems and total unimodularity
- Multi-commodity flows for multiple freight types
- Pyomo implementation patterns
- Complete working examples with explanations

### Solver Setup
- **Solver**: GLPK (installed via `sudo apt-get install glpk-utils` or `conda install -c conda-forge glpk`)
- **Verify**: `glpsol --version`
- **Test**: `python src/optimization/assignment_example.py`

## Development Workflow

### Environment Setup
```bash
# Automated setup
bash scripts/env-setup.sh
conda activate railopt  # or your env name

# Verify optimization stack
glpsol --version
python -c "import pyomo; print(pyomo.__version__)"
```

### Working with Documentation
- **Setup**: [docs/setup.md](setup.md) - Complete environment configuration
- **Optimization**: [docs/railway-optimization.md](railway-optimization.md) - Theory & code
- **Data**: [docs/data-workflow.md](data-workflow.md) - DataCatalog patterns
- **Notebooks**: [docs/notebook-guide.md](notebook-guide.md) - Best practices

### DataCatalog Usage
```python
from generic.helpers import create_data_catalog

catalog = create_data_catalog('.')
catalog.find_files('pattern')     # Search files
df = catalog.load_file('name')    # Auto-format detection
```

## Development Commands

```bash
# Environment
conda activate railopt
bash scripts/env-setup.sh  # Initial setup

# Run optimization examples
python src/optimization/assignment_example.py
python src/optimization/railway_routing_simple.py
python src/optimization/dataset_preparation.py

# Jupyter
jupyter notebook  # or jupyter lab
```

## Windows Compatibility

- Use pathlib for cross-platform paths
- UTF-8 encoding: `pd.read_csv('file.csv', encoding='utf-8')`
- Avoid special characters in filenames
- Git Bash recommended for setup script

## Notes

- Project follows cookiecutter-data-science conventions with railway-specific enhancements
- Environment managed via conda + requirements.txt
- Focus on reproducible research workflows
- All src/ directories are proper Python packages (have `__init__.py`)
- Optimization models use Pyomo with GLPK solver backend
