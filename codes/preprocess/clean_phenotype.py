import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the phenotype data
phenotype = pd.read_excel(r'C:\Users\adayc\Desktop\code\Drug\DA_data\DA_phenotype.xlsx')

# Remove specific columns with personal information
phenotype = phenotype.drop(columns=['brigade', 'IDNUM']) # add more columns if needed

# Separate rows with "type" 1: DA; 2: Healthy
type1 = phenotype[phenotype['type'] == 1]
type2 = phenotype[phenotype['type'] == 2]
type1.columns = phenotype.columns
type2.columns = phenotype.columns

# Rename the healthy group ID
type2['ID'] = [f"HP{index+1:03}" for index in range(len(type2))]

# Remove rows with specific IDs in DA group (data missing or not reliable)
excluded_ids = ['DA148', 'DA163', 'DA196']
type1 = type1[~type1['ID'].isin(excluded_ids)]

# Save the cleaned data
da_output_path = r'C:\Users\adayc\Desktop\code\Drug\DA_data\only_DA_phenotype.xlsx'
healthy_output_path = r'C:\Users\adayc\Desktop\code\Drug\DA_data\healthy_phenotype.xlsx'
type1.to_excel(da_output_path, index=False)
type2.to_excel(healthy_output_path, index=False)
print(f"DA table saved to {da_output_path}")
print(f"Non-DA table saved to {healthy_output_path}")