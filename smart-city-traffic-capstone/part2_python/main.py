import argparse
import logging
import sys
import pandas as pd

from feature_engineering import create_features
from visualization import generate_visualizations

def setup_logging(debug: bool = False):
    import warnings
    warnings.filterwarnings('ignore')
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("pipeline.log", mode='a'),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

def main():
    parser = argparse.ArgumentParser(description="Smart City Traffic Analytics CLI (NUS Capstone Part 2)")
    parser.add_argument('--debug', action='store_true', help='Enable DEBUG level logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Available CLI commands')
    
    # --- Task 1-3 Pipeline Commands ---
    subparsers.add_parser('features', help='Run feature engineering')
    subparsers.add_parser('visualize', help='Generate analysis figures')
    subparsers.add_parser('run-all', help='Execute entire pipeline')
    
    # --- Task 4 Analytics Query Commands ---
    # Query 1: Specific Date/Time Traffic
    p_query = subparsers.add_parser('query-datetime', help='Query traffic for a specific date (YYYY-MM-DD)')
    p_query.add_argument('--date', required=True, help='Date in format YYYY-MM-DD')
    
    # Query 2: High Traffic Periods
    p_high = subparsers.add_parser('high-traffic', help='Identify high traffic periods above volume threshold')
    p_high.add_argument('--threshold', type=int, default=5000, help='Traffic volume threshold')
    
    # Query 3: Weekday vs Weekend Summary
    subparsers.add_parser('compare-daytype', help='Compare weekday vs weekend average traffic')

    args = parser.parse_args()
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    # Log command and arguments (INFO requirement)
    if args.command:
        logger.info(f"Command invoked: '{args.command}' with arguments: {vars(args)}")

    try:
        if args.command in ['features', 'visualize', 'run-all']:
            if args.command == 'features':
                df = pd.read_csv('cleaned_traffic_data.csv')
                create_features(df).to_csv('featured_traffic_data.csv', index=False)
            elif args.command == 'visualize':
                generate_visualizations()
            elif args.command == 'run-all':
                df = pd.read_csv('cleaned_traffic_data.csv')
                create_features(df).to_csv('featured_traffic_data.csv', index=False)
                generate_visualizations()

        elif args.command == 'query-datetime':
            # Input Validation for Date
            try:
                valid_date = pd.to_datetime(args.date).strftime('%Y-%m-%d')
            except Exception:
                logger.error(f"Invalid date format supplied: '{args.date}'. Expected format: YYYY-MM-DD.")
                sys.exit(1)

            df = pd.read_csv('featured_traffic_data.csv')
            result = df[df['date_time'].str.startswith(valid_date)]
            
            if result.empty:
                logger.warning(f"No traffic record found for date: {valid_date}")
            else:
                print(f"\n--- Traffic Summary for {valid_date} ---")
                print(result[['date_time', 'traffic_volume', 'temp_celsius', 'congestion_level']].head(10).to_string(index=False))

        elif args.command == 'high-traffic':
            df = pd.read_csv('featured_traffic_data.csv')
            high_df = df[df['traffic_volume'] >= args.threshold]
            print(f"\n--- Found {len(high_df)} high-traffic records (>= {args.threshold}) ---")
            print(high_df[['date_time', 'traffic_volume', 'is_weekend', 'congestion_level']].head(10).to_string(index=False))

        elif args.command == 'compare-daytype':
            df = pd.read_csv('featured_traffic_data.csv')
            summary = df.groupby('is_weekend')['traffic_volume'].agg(['mean', 'median', 'std', 'max']).reset_index()
            summary['is_weekend'] = summary['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
            print("\n--- Weekday vs Weekend Traffic Summary ---")
            print(summary.to_string(index=False))

        else:
            parser.print_help()

    except FileNotFoundError as e:
        logger.error(f"Data file missing: {e}. Please run 'run-all' or 'features' first.")
    except Exception as e:
        logger.error(f"Unexpected error occurred during execution: {str(e)}")

if __name__ == "__main__":
    main()