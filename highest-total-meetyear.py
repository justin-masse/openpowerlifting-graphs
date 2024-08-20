import csv

def safe_convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_convert_to_decimal(value):
    try:
        if value is None or value.strip() == '':
            return None
        return float(value)
    except (ValueError, TypeError):
        return None

def filter_and_prepare_item(row):
    # Extract the year from the Date
    meet_year = row['Date'][:4]
    meet_year_int = safe_convert_to_int(meet_year)

    # Apply filters
    if (meet_year_int >= 2010 and
        # row['Sex'] == 'M' and
        row['Event'] == 'SBD'):
        # row['Equipment'] in ['Raw', 'Wraps']):

        # Prepare the item to be written to new CSV
        item = {
            "Name": row['Name'],
            "MeetYear": meet_year_int,
            "Equipment": row['Equipment'],
            "Age": safe_convert_to_int(row['Age']),
            "AgeClass": row['AgeClass'] if row['AgeClass'] else 'unknown',
            "BodyweightKg": safe_convert_to_decimal(row['BodyweightKg']),
            "WeightClassKg": safe_convert_to_decimal(row['WeightClassKg']),
            "TotalKg": safe_convert_to_decimal(row['TotalKg']),
            "Dots": safe_convert_to_decimal(row['Dots']),
            "Date": row['Date'],
        }
        return item
    return None

def write_to_csv(filtered_items, output_file_path):
    if not filtered_items:
        print("No items matched the filter criteria.")
        return

    # Define the header based on item keys
    header = filtered_items[0].keys()

    with open(output_file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(filtered_items)

def process_csv(input_file_path, output_file_path):
    unique_items = {}
    with open(input_file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = filter_and_prepare_item(row)
            if item and 'TotalKg' in item and item['TotalKg']:
                key = (item['Name'], item['MeetYear'], item['WeightClassKg'])
                existing_item = unique_items.get(key)
                if existing_item:
                    # Compare TotalKg to keep the highest one, handling None values
                    current_total_kg = item['TotalKg']
                    existing_total_kg = existing_item['TotalKg']
                    
                    if current_total_kg is not None and (
                        existing_total_kg is None or
                        current_total_kg > existing_total_kg
                    ):
                        unique_items[key] = item
                else:
                    unique_items[key] = item

    # Convert unique_items values to a list for writing
    filtered_items = list(unique_items.values())

    write_to_csv(filtered_items, output_file_path)

# Example usage
input_file_path = 'powerlifting_data.csv'
output_file_path = 'sbd_2010.csv'
process_csv(input_file_path, output_file_path)