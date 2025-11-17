# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv('blade_data.csv')
df['Price'] = df['Price'].str.replace('$', '', regex=False) \
                         .str.replace(' ', '', regex=False) \
                         .astype(float)

# Data normalization function
def normalize(df, categories):
    for category in categories:
        min_val = df[category].min()
        max_val = df[category].max()
        df[category] = 10 * (df[category] - min_val) / (max_val - min_val)
    return df

# Define the categories to analyze
categories = ['Speed', 'Control', 'Stiffness', 'Hardness', 'Consistency', 'Price']

# Normalize data
df = normalize(df, categories)

# Function to create a radar chart
def create_radar_chart(df, blade_name):
    row = df[df['Blade'] == blade_name].iloc[0]
    
    values = row[categories].values.flatten().tolist()
    values += values[:1]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    
    plt.xticks(angles[:-1], categories)
    plt.title(f'Radar Chart for {blade_name}')
    
    plt.show()

# Interactive display function
def show_blade_chart():
    # Display all available blade names
    print("Available blade models:")
    for i, blade in enumerate(df['Blade'], 1):
        print(f"{i}. {blade}")
    
    while True:
        try:
            choice = input("\nPlease enter the blade number (or enter 'q' to quit): ")
            if choice.lower() == 'q':
                print("Program exited")
                break
            
            blade_index = int(choice) - 1
            if 0 <= blade_index < len(df['Blade']):
                selected_blade = df['Blade'].iloc[blade_index]
                create_radar_chart(df, selected_blade)
            else:
                print("Invalid selection, please enter a number between 1 and {}".format(len(df['Blade'])))
        except ValueError:
            print("Please enter a valid number")

# Run the program
if __name__ == "__main__":
    show_blade_chart()
