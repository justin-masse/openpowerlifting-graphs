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
    if (meet_year_int >= 2004 and
        row['Sex'] == 'M' and
        row['Event'] == 'SBD' and
        row['Equipment'] in ['Raw', 'Wraps']):
        
        # Prepare the item to be written to new CSV
        item = {
            "Name": row['Name'],
            "MeetYear": meet_year_int,
            "Equipment": row['Equipment'],
            "Age": safe_convert_to_int(row['Age']),
            "AgeClass": row['AgeClass'],
            "BirthYearClass": row['BirthYearClass'],
            "Division": row['Division'],
            "BodyweightKg": safe_convert_to_decimal(row['BodyweightKg']),
            "WeightClassKg": safe_convert_to_decimal(row['WeightClassKg']),
            "Squat1Kg": safe_convert_to_decimal(row['Squat1Kg']),
            "Squat2Kg": safe_convert_to_decimal(row['Squat2Kg']),
            "Squat3Kg": safe_convert_to_decimal(row['Squat3Kg']),
            "Best3SquatKg": safe_convert_to_decimal(row['Best3SquatKg']),
            "Bench1Kg": safe_convert_to_decimal(row['Bench1Kg']),
            "Bench2Kg": safe_convert_to_decimal(row['Bench2Kg']),
            "Bench3Kg": safe_convert_to_decimal(row['Bench3Kg']),
            "Best3BenchKg": safe_convert_to_decimal(row['Best3BenchKg']),
            "Deadlift1Kg": safe_convert_to_decimal(row['Deadlift1Kg']),
            "Deadlift2Kg": safe_convert_to_decimal(row['Deadlift2Kg']),
            "Deadlift3Kg": safe_convert_to_decimal(row['Deadlift3Kg']),
            "Best3DeadliftKg": safe_convert_to_decimal(row['Best3DeadliftKg']),
            "TotalKg": safe_convert_to_decimal(row['TotalKg']),
            "Dots": safe_convert_to_decimal(row['Dots']),
            "Country": row['Country'],
            "State": row['State'],
            "Federation": row['Federation'],
            "ParentFederation": row['ParentFederation'],
            "Date": row['Date'],
            "MeetCountry": row['MeetCountry'],
            "MeetName": row['MeetName'],
            "Sanctioned": row['Sanctioned']
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
            if item:
                key = (item['Name'], item['MeetYear'])
                if key not in unique_items:
                    unique_items[key] = item
                else:
                    print(f"Duplicate found and skipped: {item}")

    # Convert unique_items values to a list for writing
    filtered_items = list(unique_items.values())

    write_to_csv(filtered_items, output_file_path)

# Example usage
input_file_path = 'powerlifting_data.csv'
output_file_path = 'filtered_powerlifting_data.csv'
process_csv(input_file_path, output_file_path)