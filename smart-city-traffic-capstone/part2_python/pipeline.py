import sys
import logging
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. Logger Setup (Module-level Logger)
# ---------------------------------------------------------
logger = logging.getLogger(__name__)

def configure_logging(log_filename="pipeline.log"):
    """Configures handlers and formatters for the module logger."""
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # File Handler for Audit Trail
        file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        
        # Console Handler for Monitoring
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

# ---------------------------------------------------------
# 2. Pipeline Execution Functions
# ---------------------------------------------------------
EXPECTED_COLUMNS = [
    'date_time', 'holiday', 'temp', 'rain_1h', 
    'snow_1h', 'clouds_all', 'weather_main', 
    'weather_description', 'traffic_volume'
]

def load_data(file_path: str) -> pd.DataFrame:
    """Loads CSV file safely using specific exception handling."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded raw dataset from '{file_path}'. Dimensions: {df.shape[0]} rows, {df.shape[1]} columns.")
        return df
    except FileNotFoundError as e:
        logger.error(f"File loading failed: File not found at '{file_path}'.", exc_info=True)
        sys.exit(1)
    except pd.errors.EmptyDataError as e:
        logger.error(f"File loading failed: The file at '{file_path}' is empty.", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error occurred while loading '{file_path}'.", exc_info=True)
        sys.exit(1)

def validate_schema(df: pd.DataFrame) -> None:
    """Validates that all expected columns are present in the dataset."""
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        logger.error(f"Schema validation failed. Missing expected columns: {missing_cols}", exc_info=True)
        sys.exit(1)
    logger.info("Schema validation passed. All expected columns are present.")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Executes multi-stage data cleaning with individual step logging."""
    df_clean = df.copy()

    # Step A: Standardise Categorical Values
    if 'weather_main' in df_clean.columns:
        df_clean['weather_main'] = df_clean['weather_main'].astype(str).str.strip().str.title()
        logger.info("Standardised categorical column 'weather_main' (stripped whitespace, title-cased).")

    # Step B: Parse Datetime Fields
    try:
        df_clean['date_time'] = pd.to_datetime(df_clean['date_time'])
        logger.info("Parsed and validated 'date_time' field into datetime64 format.")
    except Exception as e:
        logger.error("Failed to parse 'date_time' column into datetime format.", exc_info=True)
        sys.exit(1)

    # Step C: Remove Duplicates
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    dropped_duplicates = initial_count - len(df_clean)
    if dropped_duplicates > 0:
        logger.warning(f"Dropped {dropped_duplicates} duplicate rows from the dataset. Remaining rows: {len(df_clean)}.")
    else:
        logger.info("Duplicate check completed. No duplicate rows detected.")

    # Step D: Handle Temperature Outliers (0 Kelvin / < 200 K) via Monthly Median Loop
    df_clean['month'] = df_clean['date_time'].dt.month
    invalid_temp_mask = df_clean['temp'] < 200.0  # Physical outlier threshold
    affected_temp_rows = invalid_temp_mask.sum()

    if affected_temp_rows > 0:
        logger.warning(f"Detected {affected_temp_rows} rows with invalid temperature (<200 K / 0 Kelvin anomaly). Imputing by monthly median.")
        unique_months = df_clean['month'].unique()
        
        # Explicit loop over groups for monthly imputation
        for m in unique_months:
            valid_monthly_median = df_clean.loc[(df_clean['month'] == m) & (~invalid_temp_mask), 'temp'].median()
            impute_target_mask = (df_clean['month'] == m) & invalid_temp_mask
            imputed_count = impute_target_mask.sum()
            if imputed_count > 0:
                df_clean.loc[impute_target_mask, 'temp'] = valid_monthly_median
                logger.info(f"Imputed {imputed_count} temperature outliers for Month {m} using median value: {valid_monthly_median:.2f} K.")

    # Step E: Handle Rainfall Outliers (> 9,000 mm) via Monthly Median Loop
    invalid_rain_mask = df_clean['rain_1h'] > 9000.0  # Physically implausible threshold
    affected_rain_rows = invalid_rain_mask.sum()

    if affected_rain_rows > 0:
        logger.warning(f"Detected {affected_rain_rows} rows with impossible rainfall (>9000 mm). Imputing by monthly median.")
        for m in df_clean['month'].unique():
            valid_rain_median = df_clean.loc[(df_clean['month'] == m) & (~invalid_rain_mask), 'rain_1h'].median()
            impute_target_mask = (df_clean['month'] == m) & invalid_rain_mask
            imputed_count = impute_target_mask.sum()
            if imputed_count > 0:
                df_clean.loc[impute_target_mask, 'rain_1h'] = valid_rain_median
                logger.info(f"Imputed {imputed_count} rainfall outliers for Month {m} using median value: {valid_rain_median:.2f} mm.")

    df_clean = df_clean.drop(columns=['month'])
    logger.info(f"Data cleaning pipeline successfully executed. Final dataset size: {len(df_clean)} rows.")
    return df_clean

# ---------------------------------------------------------
# 3. Main Execution Entry Point
# ---------------------------------------------------------
def main():
    configure_logging()
    logger.info("================ Starting Traffic Data Pipeline ================")
    
    raw_file_path = "Metro_Interstate_Traffic_Volume.csv"
    
    raw_df = load_data(raw_file_path)
    validate_schema(raw_df)
    clean_df = clean_data(raw_df)
    
    clean_df.to_csv("cleaned_traffic_data.csv", index=False)
    logger.info("Cleaned dataset exported to 'cleaned_traffic_data.csv'. Pipeline finished successfully.")

if __name__ == "__main__":
    main()