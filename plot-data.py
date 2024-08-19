import json
import matplotlib.pyplot as plt

# Load the data from the JSON file
with open('weightclass-data.json', 'r') as file:
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
    mean_total_kgs = []
    # median_total_kgs = []

    # Extract the data for the current weight class
    for entry in data[weight_class]:
        meetYearInt = int(entry['meetYear'])
        if(meetYearInt < 2010):
            continue
        years.append(entry['meetYear'])
        mean_total_kgs.append(entry['meanTotalKg'])
        # median_total_kgs.append(entry['medianTotalKg'])

    # Plot meanTotalKg and medianTotalKg lines
    plt.plot(years, mean_total_kgs, color=colors[i], marker=markers[i], linestyle='-', label=f'{weight_class} Average Total Kg')
    # plt.plot(years, median_total_kgs, color=colors[i], marker=markers[i], linestyle='--', label=f'{weight_class} Median TotalKg')

# Add labels and title
plt.xlabel('Meet Year')
plt.ylabel('Total Kg')
plt.title('Average Total Kg by Weight Class Over 20 Years (top 200 lifters in each class)')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig('weightclass_plot.png')

# Show the plot
plt.show()