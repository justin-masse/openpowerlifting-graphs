import json
import matplotlib.pyplot as plt

# Load the data from the JSON file
with open('total-lifters.json', 'r') as file:
    data = json.load(file)

# Create a new figure
plt.figure(figsize=(12, 8))

# Define weight classes and their colors
weight_classes = ["75kg", "82.5kg", "90kg", "100kg"]
colors = ['b', 'g', 'r', 'c']
markers = ['o', '^', 's', 'D']

# Plot data for each weight class
for i, weight_class in enumerate(weight_classes):
    years = []
    totalLifters = []

    # Extract the data for the current weight class
    for entry in data[weight_class]:
        meetYearInt = int(entry['meetYear'])
        if(meetYearInt == 2024 or meetYearInt < 2014 or meetYearInt == 2020 or meetYearInt == 2021):
            continue
        years.append(entry['meetYear'])
        totalLifters.append(entry['totalLifters'])

    # Plot meanTotalKg and medianTotalKg lines
    plt.plot(years, totalLifters, color=colors[i], marker=markers[i], linestyle='-', label=f'{weight_class} Total Lifters')

# Add labels and title
plt.xlabel('Meet Year')
plt.ylabel('Total Lifters in Weightclass')
plt.title('Total Lifters by Weight Class Over Years')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig('lifters_by_weightclass.png')

# Show the plot
plt.show()