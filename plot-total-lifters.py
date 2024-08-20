import json
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the JSON file
with open('total-lifters.json', 'r') as file:
    data = json.load(file)

# Define weight classes and their colors
weight_classes = ["75kg", "82.5kg", "90kg", "100kg"]
colors = ['b', 'g', 'r', 'c']
line_styles = ['-', '--', '-.', ':']

# Collect all years to synchronize x-axis positions
all_years = sorted(list({entry['meetYear'] for wc in weight_classes for entry in data[wc]}))

# Create a new figure
plt.figure(figsize=(16, 10))

# Plot data for each weight class
for i, weight_class in enumerate(weight_classes):
    years = []
    totalLifters = []
    rawLifters = []
    equippedLifters = []

    # Extract the data for the current weight class
    for year in all_years:
        entry = next((e for e in data[weight_class] if e['meetYear'] == year), None)
        if entry and int(entry['meetYear']) >= 2010:
            years.append(year)
            totalLifters.append(entry['totalLifters'])
            rawLifters.append(entry['rawLifters'])
            equippedLifters.append(entry['equippedLifters'])
        else:
            years.append(year)
            totalLifters.append(0)
            rawLifters.append(0)
            equippedLifters.append(0)

    # Plot lines for each type of lifter
    plt.plot(years, totalLifters, color=colors[i], linestyle=line_styles[0], marker='o', label=f'{weight_class} Total Lifters')
    plt.plot(years, rawLifters, color=colors[i], linestyle=line_styles[1], marker='s', label=f'{weight_class} Raw Lifters')
    plt.plot(years, equippedLifters, color=colors[i], linestyle=line_styles[2], marker='^', label=f'{weight_class} Equipped Lifters')

# Add labels and title
plt.xlabel('Meet Year')
plt.ylabel('Number of Lifters')
plt.title('Trends of Total, Raw, and Equipped Lifters by Weight Class Over Years')

# Add legend and grid
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig('lifters_by_weightclass_line.png')

# Show the plot
plt.show()