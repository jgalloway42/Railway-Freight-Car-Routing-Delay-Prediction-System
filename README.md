# Railway Freight Car Routing & Delay Prediction System

An integrated system for optimizing freight car routing and predicting delays in railway networks using mixed-integer linear programming (MILP) and machine learning. Built on a professional data science template framework for reproducible research and production-ready code.

**Key Capabilities:**
- **Optimization Engine**: Multi-commodity network flow routing using Pyomo and GLPK
- **ML-based Prediction**: Delay prediction models trained on historical routing data
- **Professional Framework**: Reproducible workflows with DataCatalog and structured project organization

## Key Features

### 🗂️ **Organized Project Structure**
- **`src/`** - Modular source code organized by functionality
- **`data/`** - Structured data storage (raw, processed, interim, external)
- **`notebooks/`** - Jupyter notebooks with pre-configured template
- **`models/`** - Trained models and artifacts
- **`reports/figures/`** - Generated visualizations

### 📊 **DataCatalog System**
- Automatic file discovery across data directories
- Smart file loading with format detection (CSV, Excel, JSON, Pickle, Parquet, HDF5)
- File search and filtering capabilities
- Metadata tracking (size, modification dates, paths)

### 📓 **Template Notebook**
- Pre-configured with all essential imports
- Automatic DataCatalog initialization
- Clean, explicit import structure
- Ready-to-use data science environment

### 🛠️ **Helpful Utilities**
- **Visualization functions** with caching and export options
- **File operations** with joblib serialization
- **Data manipulation helpers** for common tasks
- **Path management** with robust project root detection

## Quick Start

**Get up and running in 3 steps:**

1. **Clone/download this template**
2. **Run setup script**: `bash scripts/env-setup.sh`
3. **Start analyzing**: Open `notebooks/zz_template_notebook.ipynb`

👉 **See [docs/setup.md](docs/setup.md) for detailed setup instructions**

## Project Structure

```
├── README.md          ← Project overview (you are here)
├── requirements.txt   ← Python package dependencies
├── scripts/
│   └── env-setup.sh   ← Environment setup script
├── data/
│   ├── raw/           ← Original, immutable data
│   ├── processed/     ← Final datasets for modeling
│   └── interim/       ← Intermediate transformed data
├── notebooks/
│   └── zz_template_notebook.ipynb  ← Pre-configured analysis template
├── src/               ← Source code for this project
│   ├── generic/       ← Core utilities and imports
│   ├── optimization/  ← Railway routing optimization models (Pyomo/GLPK)
│   ├── data_prep/     ← Data preparation modules
│   ├── features/      ← Feature engineering
│   ├── models/        ← ML model training and evaluation
│   └── visualization/ ← Custom plotting functions
├── models/            ← Trained models and artifacts
├── reports/figures/   ← Generated visualizations
└── docs/              ← Detailed documentation and guides
    └── railway-optimization.md  ← MILP theory and implementation guide
```

## Documentation

### Getting Started
- **[docs/setup.md](docs/setup.md)** - Complete setup guide with troubleshooting

### Railway Optimization
- **[docs/railway-optimization.md](docs/railway-optimization.md)** - MILP fundamentals, network flow theory, and Pyomo implementation
- **Working examples** in `src/optimization/`: assignment problems, multi-commodity flows, dataset generation

### Development
- **[docs/data-workflow.md](docs/data-workflow.md)** - DataCatalog system and data management
- **[docs/notebook-guide.md](docs/notebook-guide.md)** - Jupyter notebook best practices

### AI Assistant
- **[.claude/CLAUDE.md](.claude/CLAUDE.md)** - Guide for Claude Code and AI assistants

## Based On

This template extends the proven [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science) structure with additional utilities and modern Python practices.

## Next Steps

1. 📖 Read the [setup guide](docs/setup.md) to get your environment configured
2. 🎯 Study [railway optimization fundamentals](docs/railway-optimization.md) for MILP theory
3. 🚂 Run the examples in `src/optimization/` to see routing in action
4. 📊 Explore the template notebook for data analysis workflows
5. 📚 Browse the [detailed documentation](docs/) for advanced usage