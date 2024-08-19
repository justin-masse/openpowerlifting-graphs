import csv
import boto3
from decimal import Decimal, InvalidOperation

# Specify your AWS profile name here
profile_name = 'justin-ddb'
# Initialize a session using the specified profile
session = boto3.Session(profile_name=profile_name)

# Initialize the DynamoDB resource using the session
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table_name = "openpowerlifting-test"
table = dynamodb.Table(table_name)

def safe_convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None

def safe_convert_to_decimal(value):
    try:
        # Ensure the value is not empty or None
        if value is None or value.strip() == '':
            return None
        # Attempt conversion to Decimal
        return Decimal(value)
    except (ValueError, InvalidOperation, TypeError):
        return None

def filter_and_prepare_item(row):
    # Extract the year from the Date
    meet_year = row['Date'][:4]
    meet_year_int = safe_convert_to_int(meet_year)

    # Prepare the item to be inserted into DynamoDB
    return {
        "Name": row['Name'],
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
        "Federation": row['Federation'],
        "ParentFederation": row['ParentFederation'],
        "Date": row['Date'],
        "MeetYear": meet_year_int,
        "MeetName": row['MeetName'],
        "Sanctioned": row['Sanctioned']
    }


def write_to_dynamodb(items):
    # Track unique items by Name and Date
    unique_items = {}
    for item in items:
        key = (item['Name'], item['Date'])
        if key not in unique_items:
            unique_items[key] = item
        else:
            print(f"Duplicate found and skipped: {item}")

    with table.batch_writer() as batch:
        for item in unique_items.values():
            batch.put_item(Item=item)

def process_csv(file_path):
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        items_to_write = []
        for row in reader:
            item = filter_and_prepare_item(row)
            if item:
                items_to_write.append(item)

        if items_to_write:
            write_to_dynamodb(items_to_write)
        else:
            print("No items matched the filter criteria.")

# Example usage
process_csv('filtered_powerlifting_data.csv')