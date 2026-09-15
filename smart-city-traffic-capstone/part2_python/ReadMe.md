# Smart City Traffic Analytics Pipeline (NUS Capstone Part 2)

A production-grade, modular Python command-line interface (CLI) application designed for automated data processing, feature engineering, statistical visualization, and interactive traffic data querying. 

This repository adheres to strict software engineering standards, environment isolation, and dual-mode audit logging.

---

## 1. System Architecture & Directory Structure

The project is decoupled into single-responsibility modules to ensure code reusability, maintainability, and headless execution readiness.

```text
part2_python/
├── .venv/                      # Isolated Python 3.12 virtual environment
├── outputs/                    # Generated figure deliverables
│   ├── traffic_hourly_demand.png
│   ├── traffic_distribution_congestion.png
│   └── traffic_weather_relationship.png
├── cleaned_traffic_data.csv    # Initial clean dataset
├── featured_traffic_data.csv   # Post-feature engineering dataset
├── pipeline.log                # Persistent operational & audit log
├── data_cleaning.py            # Task 1: Preprocessing logic
├── feature_engineering.py      # Task 1 & 2: Feature creation module
├── visualization.py            # Task 3: Statistical plot generator
├── main.py                     # Task 4: CLI Application entry-point
├── README.md                   # System documentation & usage guide
├── TECHNICAL_REPORT.md         # Final written report submission
└── DEBUGGING.md                # V&V technical debugging trail

Data Pipeline Flow
Raw CSV ➔ data_cleaning.py ➔ cleaned_traffic_data.csv
                                 			      ▼
                     			 feature_engineering.py ➔ featured_traffic_data.csv
                  		┌──────┴──────┐
                 		 ▼                                 		▼
          		 visualization.py                      main.py (CLI App)
      		                │                                 		│
                  		▼                                 		▼
           		outputs/*.png                      pipeline.log & Terminal Output

2. Environment Setup & Execution
To prevent Interpreter Drift and package contamination across host environments, explicitly invoke the local Virtual Environment Python executable:
# Verify Python version isolation (3.12.x expected)
.\.venv\Scripts\python.exe --version

# Install dependencies within the isolated virtual environment
.\.venv\Scripts\python.exe -m pip install pandas numpy scikit-learn matplotlib seaborn
3. Command-Line Reference (main.py)
The application exposes operational pipeline tasks and analytics queries through a subcommand architecture built on argparse.
Command	Arguments	Level	Description
features	--input, --output	Pipeline	Runs feature engineering and logs quantile cut-offs.
visualize	--input, --output-dir	Pipeline	Generates and exports all 3 statistical figures.
run-all	--debug	Pipeline	Executes end-to-end processing with verbose audit logging.
query-datetime	--date YYYY-MM-DD	Analytics	Queries traffic metrics for a specific date.
high-traffic	--threshold [INT]	Analytics	Filters records exceeding specified traffic volume.
compare-daytype	None	Analytics	Aggregates traffic stats comparing Weekdays vs. Weekends.

Operational Usage Examples
PowerShell
# 1. Execute feature engineering with DEBUG audit logs
.\.venv\Scripts\python.exe main.py --debug features

# 2. Generate visualization figures
.\.venv\Scripts\python.exe main.py visualize

# 3. Execute full end-to-end pipeline
.\.venv\Scripts\python.exe main.py run-all

# 4. Query traffic metrics for a specific date
.\.venv\Scripts\python.exe main.py query-datetime --date "2018-09-14"

# 5. Filter high-traffic periods (Volume >= 5000)
.\.venv\Scripts\python.exe main.py high-traffic --threshold 5000

# 6. Aggregate Weekday vs. Weekend traffic summary
.\.venv\Scripts\python.exe main.py compare-daytype
4. Logging & Defensive Safety
•	Audit Trail (pipeline.log): High-level operational events write to INFO. Internal calculations (e.g., quantile cut-offs) write to DEBUG.
•	Defensive Failure Guardrails: Malformed inputs (such as invalid date strings) are intercepted cleanly, generating an ERROR log entry without crashing the application or emitting raw tracebacks.

