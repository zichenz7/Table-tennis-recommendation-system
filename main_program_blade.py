import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('blade_data.csv')
df['Price'] = df['Price'].str.replace('$', '', regex=False) \
                         .str.replace(' ', '', regex=False) \
                         .astype(float)
print("Data loading complete...")

# Data normalization function
def normalize(df, categories):
    df_normalized = df.copy()
    for category in categories:
        min_val = df[category].min()
        max_val = df[category].max()
        df_normalized[category] = 10 * (df[category] - min_val) / (max_val - min_val)
    return df_normalized

# Function to create radar chart
def create_radar_chart(df, blade_name, categories):
    row = df[df['Blade'] == blade_name].iloc[0]
    
    values = row[categories].values.flatten().tolist()
    values += values[:1]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    
    plt.xticks(angles[:-1], categories)
    plt.title(f'Performance Analysis for {blade_name}')
    
    return fig

# Other functions remain unchanged...
def get_importance_value(choice):
    importance_values = {
        'A': 4,  # Very important
        'B': 3,  # Important
        'C': 2,  # Less important
        'D': 1   # Not important at all
    }
    return importance_values.get(choice.upper(), 2)

def get_user_preferences():
    criteria = ["Speed", "Control", "Stiffness", "Hardness", "Consistency", "Price"]
    comparison_matrix = np.ones((len(criteria), len(criteria)))
    
    print("\nPlease select the importance level for each parameter:")
    print("A. Very important")
    print("B. Important")
    print("C. Less important")
    print("D. Not important at all")
    
    user_ratings = {}
    for criterion in criteria:
        while True:
            choice = input(f"\nHow important is {criterion} to you? (A/B/C/D): ")
            if choice.upper() in ['A', 'B', 'C', 'D']:
                user_ratings[criterion] = get_importance_value(choice)
                break
            print("Invalid input, please select A, B, C, or D")
    
    return comparison_matrix

def topsis(data, weights, criteria):
    norm_data = data / np.linalg.norm(data, axis=0)
    weighted_data = norm_data * weights
    ideal_solution = np.max(weighted_data, axis=0) * criteria
    negative_ideal_solution = np.min(weighted_data, axis=0) * criteria
    distance_to_ideal = np.sqrt(np.sum((weighted_data - ideal_solution) ** 2, axis=1))
    distance_to_negative_ideal = np.sqrt(np.sum((weighted_data - negative_ideal_solution) ** 2, axis=1))
    topsis_score = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)
    return topsis_score

# Main program
print("\nWelcome to the Table Tennis Blade Recommendation System!")
print("Please answer the following questions based on your preferences, and we will recommend the best blade for you.")

# Get user input and calculate weights
categories = ["Speed", "Control", "Stiffness", "Hardness", "Consistency", "Price"]
comparison_matrix = get_user_preferences()
column_sums = comparison_matrix.sum(axis=0)
normalized_matrix = comparison_matrix / column_sums
weights = normalized_matrix.mean(axis=1)
weights_df = pd.DataFrame(weights, index=categories, columns=['Weights'])

# Prepare data and calculate ranking
df_normalized = normalize(df, categories)
df1 = df.iloc[:, [1,2,3,4,5,6,9]]
alternatives = df1.iloc[:, 0].values
data = df1.iloc[:, 1:].values
weights = np.array(weights_df['Weights'].values)
criteria = np.array([1, 1, 1, 1, 1, -1])

scores = topsis(data, weights, criteria)
ranked_indices = np.argsort(scores)[::-1]

# Create ranking DataFrame
ranking_df = pd.DataFrame({
    'Rank': range(1, len(alternatives) + 1),
    'Blade Name': alternatives[ranked_indices],
    'Score': scores[ranked_indices].round(3)
})

# Save complete results
ranking_df.to_csv('blade_ranking_results.csv', index=False)

# Display top 10 results and radar charts
print("\nBased on your preferences, here are the top 10 recommended blades:")
print("=" * 60)
print(ranking_df.head(10).to_string(index=False))
print("=" * 60)

print("\nGenerating performance analysis charts for recommended blades...")
for i in range(10):
    blade_name = ranking_df.iloc[i]['Blade Name']
    fig = create_radar_chart(df_normalized, blade_name, categories)
    plt.show()
    plt.close(fig)

print("\nThe complete ranking results have been saved to blade_ranking_results.csv")
print("Thank you for using the Table Tennis Blade Recommendation System!")
