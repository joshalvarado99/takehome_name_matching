
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the CSV files
df_document_export = pd.read_csv(r'C:\Users\joshu\Desktop\Python\Arch\document_export.csv')
df_internal_system = pd.read_csv(r'C:\Users\joshu\Desktop\Python\Arch\internal_system.csv')

# Print the first few rows of the dataframes for verification
print(df_document_export.head())
print(df_internal_system.head())

# Set similarity threshold
threshold = 40

# List to store matched pairs and scores
matched_pairs = []

# Find best match for each accountName in df_document_export with Entity Name in df_internal_system
for index, row in df_document_export.iterrows():
    account_name = row['accountName']
    account_num = row['accountNum']  # Get the accountNum to preserve
    # Find the best match in df_internal_system's 'Entity Name'
    match, score, _ = process.extractOne(account_name, df_internal_system['Entity Name'], scorer=fuzz.ratio)
    
    if score >= threshold:
        # Find the Holding ID corresponding to the matched entity name
        holding_id = df_internal_system.loc[df_internal_system['Entity Name'] == match, 'Holding ID'].values[0]
        
        matched_pairs.append({
            "Document Account Name": account_name,
            "Account Number": account_num,  # Preserve accountNum
            "Internal Entity Name": match,  # Changed to reflect new comparison
            "Holding ID": holding_id,  # Preserve Holding ID
            "Similarity Score": score
        })

# Create a DataFrame from the matched pairs
df_matches = pd.DataFrame(matched_pairs)

# Display the resulting DataFrame
print(df_matches)

# Export the matches DataFrame to a CSV file
output_file_path = r'C:\Users\joshu\Desktop\Python\Arch\matched_accounts.csv'
df_matches.to_csv(output_file_path, index=False)

print(f"Matches exported to {output_file_path}")

