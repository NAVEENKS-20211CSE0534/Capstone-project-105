import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data (replace 'your_file_path.csv' with your actual file path)
data = pd.read_csv('User_Form_Feedback - Sheet1.csv')

# Pivot the data for the heatmap
heatmap_data = data.groupby(['ProductCategory', 'BudgetRange', 'BulkInterest']).size().unstack(fill_value=0)

# Identify the product category with the highest BulkInterest
max_value = heatmap_data.max().max()
max_position = heatmap_data.stack().idxmax()

# Extract the details
max_product = max_position[0]
max_budget_range = max_position[1]
max_bulk_interest = max_position[2]

# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="coolwarm", cbar=True)
plt.title("Product Preferences by Budget Range and Bulk Interest")
plt.ylabel("Product Category")
plt.xlabel("Budget Range & Bulk Interest")
plt.xticks(rotation=45)

# Save the heatmap to an image file
plt.savefig('heatmap_output.png', format='png')

# Now, create the HTML content with the image and the highest BulkInterest product
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heatmap Output</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; }}
        img {{ max-width: 90%; height: auto; }}
    </style>
</head>
<body>
    <h1>Product Preferences by Budget Range and Bulk Interest</h1>
    
    <!-- Display the heatmap image -->
    <img src="heatmap_output.png" alt="Heatmap">
    
    <h2>Highest BulkInterest Product:</h2>
    <p>The highest preference was for <strong>{max_product}</strong> with a budget range of <strong>{max_budget_range}</strong> and Bulk Interest level of <strong>{max_bulk_interest}</strong>, with a count of <strong>{max_value}</strong>.</p>
</body>
</html>
"""

# Save the HTML content to an index.html file
# Save the HTML content to an index.html file with UTF-8 encoding
with open('app.html', 'w', encoding='utf-8') as f:
    f.write(html_content)


# Display the saved heatmap image
plt.show()
