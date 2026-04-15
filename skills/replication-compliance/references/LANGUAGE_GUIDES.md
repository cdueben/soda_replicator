# Language-Specific Reproducibility Guides

## Stata

### Essential Settings

Add these to the top of your master script (`run.do`):

```stata
version 18              // Lock Stata version behavior
clear all               // Start fresh
set more off            // Don't pause output
set varabbrev off       // Prevent variable abbreviation errors
set seed 12345          // Reproducible random numbers
```

### Path Configuration

**Never use absolute paths:**
```stata
* BAD - breaks on other computers
use "C:/Users/jsmith/Dropbox/project/data/raw/mydata.dta"

* GOOD - relative paths work everywhere
use "../data/raw/mydata.dta"

* BETTER - use globals defined in master script
global DATA "../data"
use "$DATA/raw/mydata.dta"
```

**Always use forward slashes:**
```stata
* BAD - backslashes cause issues
use "..\data\raw\mydata.dta"

* GOOD - forward slashes work on all platforms
use "../data/raw/mydata.dta"
```

### Package Management

**Option 1: Bundle packages locally (Recommended)**

Create `_install_stata_packages.do`:
```stata
* Install to project folder
local libpath "libraries/stata"
cap mkdir "`libpath'"
net set ado "`libpath'"

ssc install reghdfe, replace
ssc install ftools, replace
ssc install estout, replace
```

Configure master script to use local packages:
```stata
* Remove default ado paths
tokenize `"$S_ADO"', parse(";")
while `"`1'"' != "" {
    if `"`1'"'!="BASE" cap adopath - `"`1'"'
    macro shift
}

* Add project library
adopath ++ "$PROJECT/libraries/stata"
```

**Option 2: Document packages in README**
```markdown
## Stata Packages Required

Install before running:
- reghdfe (v6.0): `ssc install reghdfe`
- ftools: `ssc install ftools`
- estout: `ssc install estout`
```

### Ensuring Unique Sorts

Non-unique sorts produce different results across runs:

```stata
* BAD - may produce different orderings
sort firmid year

* GOOD - verify uniqueness first
isid firmid year
sort firmid year

* ALSO GOOD - use stable sort
sort firmid year, stable
```

### Assertion Checks

Add assertions to verify results haven't changed:

```stata
reg price mpg weight
assert abs(_b[mpg] - (-6.287)) < 0.01  // Coefficient check
assert e(N) == 74                       // Sample size check
```

### Useful Packages for Large Data

- `gtools` - Fast group operations
- `reghdfe` - High-dimensional fixed effects
- `ftools` - Fast data manipulation

---

## R

### Essential Settings

Add to the top of your master script (`run.R`):

```r
# Clear environment
rm(list = ls())

# Set random seed
set.seed(12345)

# Disable scientific notation (optional)
options(scipen = 999)
```

### Package Management with renv

**Initial setup:**
```r
# Initialize renv for the project
renv::init()

# Install packages as usual
install.packages("fixest")

# Snapshot package state
renv::snapshot()
```

**Replicator restores environment:**
```r
renv::restore()
```

**The `renv.lock` file records:**
- Exact package versions
- Package sources (CRAN, GitHub, etc.)
- R version

### Path Configuration

**Never use absolute paths:**
```r
# BAD
data <- read.csv("C:/Users/jsmith/project/data/raw/mydata.csv")

# GOOD - relative paths
data <- read.csv("../data/raw/mydata.csv")

# BETTER - use here package
library(here)
data <- read.csv(here("data", "raw", "mydata.csv"))
```

### Logging Session Info

Document the R environment at the end of your script:

```r
# Print session info to log
sink("session_info.txt")
sessionInfo()
sink()
```

Or at script start:
```r
cat("R version:", R.version.string, "\n")
cat("Platform:", R.version$platform, "\n")
cat("Date:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
```

### Reproducible Random Numbers

```r
# Set seed before any randomization
set.seed(12345)

# For parallel operations, use L'Ecuyer-CMRG
RNGkind("L'Ecuyer-CMRG")
set.seed(12345)
```

### Useful Packages

- `fixest` - Fast fixed effects estimation
- `data.table` - Fast data manipulation
- `modelsummary` - Publication-ready tables
- `here` - Project-relative paths
- `tictoc` - Timing code execution

---

## Python

### Essential Settings

Add to the top of your master script:

```python
import random
import numpy as np

# Set random seeds
random.seed(12345)
np.random.seed(12345)

# For TensorFlow/PyTorch
# import tensorflow as tf
# tf.random.set_seed(12345)

# import torch
# torch.manual_seed(12345)
```

### Package Management

**Option 1: requirements.txt (Recommended)**

Create `requirements.txt` with pinned versions:
```
pandas==2.1.0
numpy==1.24.0
statsmodels==0.14.0
matplotlib==3.8.0
```

Generate from current environment:
```bash
pip freeze > requirements.txt
```

Install:
```bash
pip install -r requirements.txt
```

**Option 2: conda environment.yml**

```yaml
name: myproject
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas=2.1.0
  - numpy=1.24.0
  - statsmodels=0.14.0
```

Create/restore:
```bash
conda env create -f environment.yml
conda activate myproject
```

### Path Configuration

**Never use absolute paths:**
```python
# BAD
data = pd.read_csv("C:/Users/jsmith/project/data/raw/mydata.csv")

# GOOD - relative paths
data = pd.read_csv("../data/raw/mydata.csv")

# BETTER - use pathlib
from pathlib import Path
DATA_DIR = Path(__file__).parent.parent / "data"
data = pd.read_csv(DATA_DIR / "raw" / "mydata.csv")
```

### Virtual Environments

**Create and document:**
```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

**Document in README:**
```markdown
## Python Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install packages: `pip install -r requirements.txt`
4. Run: `python run.py`
```

### Logging Environment

```python
import sys
import pkg_resources

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print("\nInstalled packages:")
for pkg in pkg_resources.working_set:
    print(f"  {pkg.project_name}=={pkg.version}")
```

---

## MATLAB

### Essential Settings

Add to the top of your master script (`main.m` or `run.m`):

```matlab
% Clear environment
clear all;
close all;
clc;

% Set random seed for reproducibility
rng(12345);

% Add project paths
addpath(genpath('functions'));
addpath(genpath('utilities'));
```

### startup.m File

Create `startup.m` in your project root:

```matlab
% startup.m - Run automatically when MATLAB opens in this directory
% Set up paths for this project

fprintf('Setting up project environment...\n');

% Add all subdirectories
addpath(genpath(pwd));

% Remove .git and other non-code folders
rmpath(genpath(fullfile(pwd, '.git')));

% Set random seed
rng(12345);

fprintf('Project environment ready.\n');
```

### Path Configuration

**Never use absolute paths:**
```matlab
% BAD
data = readtable('C:/Users/name/project/data/raw/mydata.csv');

% GOOD - relative paths
data = readtable('../data/raw/mydata.csv');

% BETTER - use fullfile for cross-platform compatibility
data_path = fullfile('..', 'data', 'raw', 'mydata.csv');
data = readtable(data_path);
```

### Toolbox Dependencies

Document required toolboxes in README:

```markdown
## MATLAB Requirements

- MATLAB R2022a or later
- Required Toolboxes:
  - Statistics and Machine Learning Toolbox
  - Optimization Toolbox
  - Econometrics Toolbox

To check if toolboxes are installed:
```matlab
ver  % List installed toolboxes
```
```

### Package/Function Management

Unlike R/Python, MATLAB doesn't have a standard package manager. Best practices:

1. **Include all custom functions** in the repository
2. **Create a `functions/` directory** for project-specific functions
3. **Document external dependencies** (MATLAB File Exchange, etc.)
4. **Use `startup.m`** to configure paths

```matlab
% Example structure
% project/
%   startup.m
%   main.m
%   functions/
%     my_estimation.m
%     my_plotting.m
%   external/
%     downloaded_package/
```

### Random Number Reproducibility

```matlab
% Set seed at script start
rng(12345);

% For specific distributions
rng(12345, 'twister');  % Mersenne Twister (default)

% Verify seed is set
s = rng;
fprintf('Random seed: %d\n', s.Seed);
```

### Useful Practices

```matlab
% Save workspace for debugging
save('checkpoint.mat');

% Document MATLAB version
fprintf('MATLAB version: %s\n', version);

% Profile code for performance
profile on;
% ... your code ...
profile viewer;
```

---

## Julia

### Essential Settings

```julia
# At top of master script
using Random
Random.seed!(12345)

# Activate project environment
using Pkg
Pkg.activate(".")
```

### Package Management

```julia
# Initialize project
Pkg.activate(".")
Pkg.instantiate()  # Install from Manifest.toml
```

**Key files:**
- `Project.toml` - Direct dependencies
- `Manifest.toml` - Complete dependency tree with versions (COMMIT THIS)

### Path Configuration

```julia
# Use joinpath for cross-platform paths
data_path = joinpath("..", "data", "raw", "mydata.csv")

# Use @__DIR__ for script-relative paths
script_dir = @__DIR__
data_path = joinpath(script_dir, "..", "data", "raw", "mydata.csv")
```

---

## Cross-Language Projects

For projects using multiple languages:

### File Formats

Use portable formats that work across languages:
- **CSV** - Universal, but loses type information
- **Parquet** - Efficient, typed, works with R/Python/Stata 18+
- **RDS/DTA** - Native formats, use `haven` (R) or `pyreadstat` (Python) to read

### Execution Order

Document clearly in README:
```markdown
## Execution Order

1. Run R scripts first (data preparation):
   ```r
   source("code/dataprep/clean_data.R")
   ```

2. Then Stata analysis:
   ```stata
   do code/analysis/regressions.do
   ```

3. Finally Python figures:
   ```bash
   python code/analysis/make_figures.py
   ```
```

### Shared Configurations

Create a config file readable by all languages:

**config.json:**
```json
{
  "seed": 12345,
  "data_path": "../data",
  "output_path": "../paper/results"
}
```

Read in each language:
```stata
* Stata (with jsonio or manually)
```

```r
# R
config <- jsonlite::read_json("config.json")
set.seed(config$seed)
```

```python
# Python
import json
with open("config.json") as f:
    config = json.load(f)
random.seed(config["seed"])
```
