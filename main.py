import sys
from pathlib import Path

from scripts.generate_sample_data import generate_sample_data
from src.data_processor import DataProcessor


def main():
    processor = DataProcessor()

    try:
        # Step 1: Generate sample data if it doesn't exist
        csv_path = Path("data/input/clientes.csv")
        if not csv_path.exists():
            print("Generating sample data...")
            df = generate_sample_data(num_records=1000)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(csv_path, index=False)
            print(f"Sample data generated to '{csv_path}'")

        # Step 2: Import customers data to database
        print("Importing customers data to database...")
        success = processor.import_csv_to_database(str(csv_path))
        if success:
            print("Import completed successfully!")
        else:
            print("Import failed!")
            sys.exit(1)

        # Step 3: Export Colombian customers
        print("\nExporting Colombian customers...")
        export_success = processor.export_colombian_customers()
        if export_success:
            print("Export completed successfully!")
        else:
            print("Export failed!")

    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
