# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# reading data files
df = pd.read_csv('rubber_data.csv')
df['Price'] = df['Price'].str.replace('$', '', regex=False) \
                         .str.replace(' ', '', regex=False) \
                         .astype(float)

# normalize data
def normalize(df, categories):
    for category in categories:
        min_val = df[category].min()
        max_val = df[category].max()
        df[category] = 10 * (df[category] - min_val) / (max_val - min_val)
    return df

# defining columns
categories = ["Speed", "Spin", "Control", "Weight", "Durable", "Price"]

# normalization
df = normalize(df, categories)

# create radar chart for individual rubber
def create_radar_chart(df, rubber_name):
    row = df[df['Rubber'] == rubber_name].iloc[0]
    
    values = row[categories].values.flatten().tolist()
    values += values[:1]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='red', alpha=0.25)
    ax.plot(angles, values, color='red', linewidth=2)
    
    plt.xticks(angles[:-1], categories)
    plt.title(f'Radar Chart for {rubber_name}')
    
    plt.show()

# user interaction
def show_rubber_chart():
    # display all rubbers' names
    print("rubber names:")
    for i, rubber in enumerate(df['Rubber'], 1):
        print(f"{i}. {rubber}")
    
    while True:
        try:
            choice = input("\ninput rubber name(or press 'q' to exit）: ")
            if choice.lower() == 'q':
                print("program terminated")
                break
            
            rubber_index = int(choice) - 1
            if 0 <= rubber_index < len(df['Rubber']):
                selected_rubber = df['Rubber'].iloc[rubber_index]
                create_radar_chart(df, selected_rubber)
            else:
                print("invalid, please input a number between 1 and{}".format(len(df['Rubber'])))
        except ValueError:
            print("please give a valid input")

# running program
if __name__ == "__main__":
    show_rubber_chart()