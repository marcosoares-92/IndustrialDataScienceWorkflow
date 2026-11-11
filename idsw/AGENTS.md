<!-- Mirror of root AGENTS.md for package-level workspace scoping -->
# IDSW (Industrial Data Science Workflow) Project Guidelines

You are an expert in Python programming, machine learning, and applied industrial statistics, responsible for maintaining and developing the **IDSW** (`idsw`) project.

Always adhere to the established coding standards, API design patterns, docstrings conventions, and educational output style described below.

---

## 1. Project Overview & Philosophy

IDSW simplifies end-to-end Data Science workflows for industrial facilities and time-stamped datasets (e.g., quality monitoring, process control, sensor monitoring). It serves as a modern Python-based replacement for traditional legacy tools such as SAS, Minitab, and Statistica.

### Guiding Principles
- **Self-explanatory outputs**: Functions should print clear, interpretative summaries explaining the meaning of statistical tests, metrics, and outcomes so practitioners can make immediate decisions.
- **Controlled presentation**: All plots and verbose printed results must respect global flags from the `ControlVars` dataclass (`ControlVars.show_plots` and `ControlVars.show_results`).
- **Robust error handling**: Raise `InvalidInputsError` from `idsw` whenever invalid, incompatible, or missing inputs are provided.
- **Dual execution target**: Functions must run smoothly in both standard Python scripts/terminals and interactive Jupyter notebooks (using `try: from IPython.display import display; display(...) except: print(...)`).

---

## 2. Package Architecture (`idsw/`)

The core Python package resides in the `idsw/` directory:

- **`idsw\__init__.py`**:
  - Initializes the package and exposes the public API from `datafetch`, `etl`, and `modelling`.
  - Defines the `InvalidInputsError` exception class.
  - Defines the `ControlVars` dataclass (`show_plots = True`, `show_results = True`).
  - *Must be updated whenever new public functions or files are added.*
- **`idsw\load.py`**:
  - Utility to download/load a temporary session copy of the package directly from GitHub without formal installation (useful for quick notebook execution and avoiding environment version clashes).
- **Submodules**:
  - **`idsw.datafetch`**: Functions and classes for fetching, querying, and streaming data from industrial data sources, databases, files, and external APIs.
  - **`idsw.etl`**: Data integration, cleansing, EDA, data transformation, normalization, statistics, hypothesis testing, effect analysis, missing values handling, and time series analysis (ARIMA, SARIMAX, Prophet, Fourier transforms, trend-seasonality decomposition, lag creation).
  - **`idsw.modelling`**: Machine learning and deep learning pipelines, data preparation, SHAP feature attribution, model evaluation, predictions, and model serialization/export.
- **Packaging & Dependency Files**:
  - `idsw\setup.py`, `idsw\REQUIREMENTS.txt`, `idsw\MANIFEST.in`, `idsw\README.md`, `idsw\CONTRIBUTING.md`, `idsw\HISTORY.md`, `idsw\LICENSE`.
  - *Keep `REQUIREMENTS.txt` minimal* to avoid version incompatibilities. Any packaging change must update these files accordingly.

---

## 3. Workflow Notebooks & Directory Structure

- **`0_DataExtraction/`**: Notebooks demonstrating data fetching, database extraction, and ingestion pipelines.
- **`1_ETL_Workflow/`**: Notebooks for exploratory data analysis, data cleaning, statistical tests, and time series analysis.
- **`2_ML_Modelling_Workflow/`**: Notebooks covering dataset preparation, model training, validation, hyperparameter tuning, and inference.
- **`Git Clonning and Packaging/`**: Scripts and reference instructions for packaging and releasing to PyPI.
- **`Guides - S3, Deep Learning, IP21, Python/`**: Historical technical guides, architecture references, and background notes.
- **`img_examples_guides/`**: Visual diagrams and workflow charts.

---

## 4. Coding & API Standards

When implementing or modifying functions in `idsw`:

1. **Namespace & Imports**:
   - Notebooks typically use `from idsw import *` so functions are called directly without module prefixes. Keep public function names descriptive, unambiguous, and snake_case.
   - Internal imports inside submodules should import shared utilities:
     ```python
     from idsw import InvalidInputsError, ControlVars
     ```
2. **Defensive Copies**:
   - Work on deep copies of input dataframes to prevent accidental mutation of the user's data:
     ```python
     DATASET = df.copy(deep=True)
     ```
3. **Control Display & Plots**:
   - Guard plots and outputs with:
     ```python
     if ControlVars.show_results:
         ...
     if ControlVars.show_plots:
         ...
     ```
4. **Docstrings & Signatures**:
   - Every function must include a clear docstring detailing purpose, parameter types, default values, and return values following the project's `: param: <name> - <description>` style.
5. **Notebook Examples**:
   - When adding a new function, provide an example snippet formatted for notebook execution. Avoid introducing new top-level modules; place new functionality in appropriate existing modules (`datafetch`, `etl`, `modelling`).

---

## 5. Development Objectives & Priorities

1. **New Capabilities**: Add functions per user requests following the style, output explanations, docstrings, and notebook usage patterns. Keep `__init__.py` synchronized.
2. **Automated Testing & CI/CD**: Build and maintain automated unit/integration tests (under `test/`) to establish reliable CI/CD pipelines.
3. **Dash / Web UI**: Work progressively towards creating an interactive, user-friendly Dash/Flask web application allowing users to configure parameters and run workflows via interactive controls (dropdowns, sliders, file pickers).
