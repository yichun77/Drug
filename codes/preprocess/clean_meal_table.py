import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
dfc = pd.read_excel(r'C:\Users\adayc\Desktop\code\Drug\DA_data\DA_daily_food_clean.xlsx')
dm = pd.read_excel(r'C:\Users\adayc\Desktop\code\Drug\DA_data\DA_daily_meal.xlsx')

# The food amount of DA163 was always 0, so we delete the DA163 data
# And we also delete DA148 and DA196 because they have missing data
# Delete other samples with missing CGM data
excluded_ids = ['DA20', 'DA65', 'DA69', 'DA129', 'DA130', 'DA155', 'DA163', 'DA148', 'DA193', 'DA196']
dfc_new = dfc[~dfc['Sampleid'].isin(excluded_ids)]
dm_new = dm[~dm['Sampleid'].isin(excluded_ids)]

# Save the cleaned data
dfc_new_output_path = r'C:\Users\adayc\Desktop\code\Drug\DA_data\filtered_DA_daily_food_clean.xlsx'
dm_new_output_path = r'C:\Users\adayc\Desktop\code\Drug\DA_data\filtered_DA_daily_meal.xlsx'
dfc_new.to_excel(dfc_new_output_path, index=False)
dm_new.to_excel(dm_new_output_path, index=False)

print(f"Filtered dfc_new saved to {dfc_new_output_path}")
print(f"Filtered dm_new saved to {dm_new_output_path}")