technical issues encountered, root-cause analyses performed, and resolution strategies implemented during the development of Part 2.

---

## 1. Environment Mismatch & Interpreter Drift

### Issue Description
Execution attempts via standard `python main.py` failed with `ModuleNotFoundError` or selected an unintended host environment. Investigation revealed that Windows system paths defaulted to a global Python 3.14 installation rather than the project's dedicated virtual environment.

```text
Host System State: Global Python 3.14 (Missing required packages)
Target Project State: Local .venv Python 3.12 (Isolated workspace)
Resolution Strategy
	Explicit Binding: Enforced execution using explicit path calls:
.\.venv\Scripts\python.exe main.py
	Environment Stabilization: Standardized configuration files to ensure dependencies resolve strictly within the local .venv path.
2. Package Dependency & Module Resolution
Issue Description
Package installation commands for scikit-learn failed to resolve when scripts imported the module using its canonical alias sklearn.
Resolution Strategy
	Targeted Package Installation: Executed explicit module installation into the virtual environment path:
.\.venv\Scripts\python.exe -m pip install scikit-learn
	Import Audit: Verified module import compatibility across scripts (from sklearn.preprocessing import ...), confirming proper package linkage within the .venv library paths.
3. Syntactic Integrity, Refactoring, & Warning Mitigation
Issue Description
	Code Structure Errors: Indentation inconsistencies in feature_engineering.py caused IndentationError exceptions during function definitions.
	Variable Scope Inconsistencies: Unclear DataFrame variable scoping (df vs. df_feat) led to intermediate state mutations.
	Library Warnings: Output streams were cluttered with FutureWarning notices from seaborn and internal configuration logs from matplotlib.
Resolution Strategy
	Code Refactoring: Standardized indentation across scripts and explicit variable isolation (df_feat = df.copy()).
	Stream Optimization: Configured warning filters and elevated library log levels in main.py to keep terminal outputs clear and focused:
Python
import warnings
import logging

# Suppress non-critical library warnings
warnings.filterwarnings('ignore')

# Silence background library loggers
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
	Log Level Separation: Established clear operational logging rules:
	INFO: Operational checkpoints (e.g., CLI command invocations, data saves).
	DEBUG: Internal mathematical thresholds (e.g., quantile cut-offs Q_33 and Q_66).
	ERROR: Input validation errors and file missing exceptions.

