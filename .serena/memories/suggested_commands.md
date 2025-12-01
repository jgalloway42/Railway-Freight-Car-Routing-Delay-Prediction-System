# Suggested Commands

## Environment Setup

### Initial Setup
```bash
# Run environment setup script (from project root)
bash scripts/env-setup.sh
```
This script will:
- Prompt for environment name and Python version
- Create conda environment
- Create data directories (raw/, processed/, interim/, external/)
- Install dependencies from requirements.txt
- Set up Jupyter kernel
- Optionally update requirements.txt with installed packages

### Environment Management
```bash
# Activate conda environment
conda activate [ENV_NAME]

# Deactivate environment
conda deactivate

# List environments
conda env list

# Update requirements.txt
pip freeze > requirements.txt
```

## Jupyter Notebooks
```bash
# Start Jupyter Notebook
jupyter notebook

# Start Jupyter Lab
jupyter lab

# Open template notebook directly
jupyter notebook notebooks/zz_template_notebook.ipynb
```

## Development Workflow
```bash
# Navigate to project directory
cd /mnt/SERENITYNAS/josue/workspace/Railway-Freight-Car-Routing-Delay-Prediction-System

# Activate environment
conda activate railopt  # or your chosen environment name

# Start Jupyter
jupyter notebook

# Work with notebooks using template as starting point
```

## Data Management
```python
# In Python/Jupyter - use DataCatalog system
from generic.helpers import create_data_catalog

# Create catalog
catalog = create_data_catalog('.')

# Browse files
catalog.list_files()

# Load data
df = catalog.load_file('your_data.csv')

# Get file path
path = catalog.get_path('your_data.csv')

# Search for files
files = catalog.find_files('pattern')
```

## System Commands (Linux)
```bash
# File operations
ls -la                    # List files with details
find . -name "*.py"      # Find Python files
grep -r "pattern" .      # Search in files

# Git operations
git status
git add .
git commit -m "message"
git push

# Directory navigation
cd [directory]
pwd                      # Print working directory
```

## Package Management
```bash
# Install new package
pip install package_name

# Install from requirements.txt
pip install -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt

# Backup requirements
cp requirements.txt requirements.txt.backup
```

## MCP/Serena Integration
```bash
# List MCP servers
claude mcp list

# Check Serena status
claude mcp get serena

# In Claude Code chat, verify MCP servers
/mcp
```

## Notes
- No formal testing, linting, or build commands - this is a research template
- Focus is on interactive development with Jupyter notebooks
- Environment managed through conda and requirements.txt
- All paths relative to project root