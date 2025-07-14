import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path


def generate_sample_data(num_records: int = 1000) -> pd.DataFrame:
    """Generate sample client data"""
    fake = Faker(['es_ES', 'en_US'])
    countries = [
        'Colombia', 'Mexico', 'Argentina', 'Chile', 'Peru', 
        'Ecuador', 'Venezuela', 'Bolivia', 'Uruguay', 'Paraguay'
    ]
    statuses = ['active', 'inactive', 'pending', 'suspended']
    data = []
    for i in range(num_records):
        # Ensure good representation of Colombian customers (25%)
        country = 'Colombia' if i % 4 == 0 else random.choice(countries)
        two_years_ago = datetime.now() - timedelta(days=365 * 2)
        record = {
            'name': fake.name(),
            'email': fake.email(),
            'country': country,
            'created_at': fake.date_time_between(
                start_date=two_years_ago,
                end_date=datetime.now()
            ),
            'status': random.choice(statuses)
        }
        data.append(record)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data(1000)
    
    # Save to CSV
    print("Generating sample data into 'data/input/clientes.csv'")
    output_path = Path('data/input/clientes.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records and saved to '{output_path}'")