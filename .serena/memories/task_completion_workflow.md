# Task Completion Workflow

## Project Type Note
This is a **data science research project template**, not a production software application. Therefore, traditional software engineering completion steps (testing, linting, building) are not applicable.

## What to Do When Task is Complete

### 1. Save Your Work
- **Notebooks**: Save Jupyter notebooks (Ctrl+S or Cmd+S)
- **Python files**: Save any modified .py files in src/
- **Data outputs**: Ensure processed data saved to appropriate data/ subdirectory
- **Models**: Save trained models to models/ directory using joblib or pickle
- **Figures**: Export visualizations to reports/figures/

### 2. Update Documentation (if needed)
- Update README.md if adding major features
- Document new functions/classes in code
- Update relevant docs/ files if workflow changes

### 3. Update Requirements (if packages added)
```bash
# Backup existing requirements
cp requirements.txt requirements.txt.backup

# Update with current environment
pip freeze > requirements.txt
```

### 4. Organize Files
- Move any test/scratch notebooks to appropriate location
- Ensure raw data stays in data/raw/ (immutable)
- Move processed datasets to data/processed/
- Clean up intermediate files in data/interim/ if no longer needed

### 5. Git Workflow (if using version control)
```bash
# Check status
git status

# Stage changes
git add [files]

# Commit with descriptive message
git commit -m "Descriptive message about changes"

# Push to remote (if applicable)
git push
```

## No Testing/Linting Required
Unlike production software:
- **No unit tests**: This is exploratory data analysis, not production code
- **No linting**: Code style is flexible for research
- **No building**: No deployment artifacts to create
- **No CI/CD**: Research project, not production system

## Focus Areas
The completion checklist for data science tasks should focus on:
1. **Reproducibility**: Can analysis be re-run?
2. **Documentation**: Are findings/methods documented?
3. **Organization**: Are files in correct directories?
4. **Version control**: Are changes committed?
5. **Requirements**: Is environment specification up to date?

## When Working on Models
If task involved model training:
- Save model artifacts to models/
- Document model parameters and performance
- Save any plots/metrics to reports/figures/
- Consider documenting approach in notebook or docs/

## When Working on Data Processing
If task involved data preparation:
- Ensure raw data untouched (data/raw/)
- Save cleaned data to data/processed/
- Document transformations applied
- Update DataCatalog if new files added