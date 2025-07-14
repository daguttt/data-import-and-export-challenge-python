# src/data_processor.py
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from src.customer_statuses import CUSTOMER_STATUSES

# Load environment variables
load_dotenv()


class DataProcessor:
    def __init__(self):
        self.db_engine = self._create_db_engine()
        self.logger = self._setup_logger()

    def _create_db_engine(self):
        """Create SQLAlchemy engine with connection parameters"""
        db_config = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
            "database": os.getenv("POSTGRES_DB", "crm"),
            "username": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", "password"),
        }

        connection_string = (
            f"postgresql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )

        return create_engine(connection_string, pool_pre_ping=True)

    def _setup_logger(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
        )
        return logging.getLogger(__name__)

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data"""
        # Remove duplicates
        df = df.drop_duplicates(subset=["email"])

        # Validate basic email format
        df = df[df["email"].str.contains("@", na=False)]

        # Convert timestamp column
        df["created_at"] = pd.to_datetime(df["created_at"])

        # Ensure status is valid
        df = df[df["status"].isin(CUSTOMER_STATUSES)]

        return df

    def import_csv_to_database(
        self, csv_file_path: str, df_chunk_size: int = 1000
    ) -> bool:
        """Import CSV data to database in dataframe chunks for memory efficiency"""
        try:
            csv_path = Path(csv_file_path)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_file_path}")

            self.logger.info(f"Starting import from {csv_file_path}")

            # For logging purposes
            chunk_count = 0
            total_rows = 0

            # Read and process CSV in chunks
            for df_chunk in pd.read_csv(csv_file_path, chunksize=df_chunk_size):
                cleaned_df_chunk = self._clean_data(df_chunk)

                cleaned_df_chunk.to_sql(
                    "customers",
                    self.db_engine,
                    if_exists="append",
                    index=False,
                    method="multi",
                )

                chunk_count += 1
                total_rows += len(cleaned_df_chunk)
                self.logger.info(
                    f"Processed chunk {chunk_count}, rows: {len(cleaned_df_chunk)}"
                )

            self.logger.info(
                f"Import completed. Total chunks: {chunk_count}, Total rows: {total_rows}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Error during import: {str(e)}")
            return False

    def export_colombian_customers(
        self, output_file_name: str = "clientes_colombia.csv"
    ) -> bool:
        """Export Colombian customers to CSV"""
        try:
            query = """
            SELECT id, name, email, country, created_at, status 
            FROM customers 
            WHERE country = 'Colombia'
            ORDER BY created_at DESC
            """

            self.logger.info("Querying Colombian customers...")
            df = pd.read_sql(query, self.db_engine)

            if df.empty:
                self.logger.warning("No Colombian customers found")
                return False

            # Export to CSV
            output_path = Path("data/output") / output_file_name
            output_path.parent.mkdir(parents=True, exist_ok=True)

            df.to_csv(output_path, index=False)
            self.logger.info(f"Exported {len(df)} Colombian customers to {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error during export: {str(e)}")
            return False

    def get_database_stats(self) -> dict:
        """Get database statistics"""
        try:
            with self.db_engine.connect() as conn:
                # Total customers
                total_query = "SELECT COUNT(*) as total FROM customers"
                total_result = conn.execute(text(total_query)).fetchone()

                # Clients by country
                country_query = """
                SELECT country, COUNT(*) as count 
                FROM customers
                GROUP BY country 
                ORDER BY count DESC
                """
                country_result = conn.execute(text(country_query)).fetchall()

                # Clients by status
                status_query = """
                SELECT status, COUNT(*) as count 
                FROM customers 
                GROUP BY status
                ORDER BY count DESC
                """
                status_result = conn.execute(text(status_query)).fetchall()

                return {
                    "total_customers": total_result[0],
                    "by_country": dict(country_result),
                    "by_status": dict(status_result),
                }

        except Exception as e:
            self.logger.error(f"Error getting stats: {str(e)}")
            return {}
