#!/usr/local/python37/bin/python3.7
# evaluate the averaged NMR chemical shifts
import os
import pandas as pd
from glob import glob

def extract_and_concatenate(file_patterns, sheet_names, writer):
    # Initialize empty DataFrames to store the data
    all_column3_df = pd.DataFrame()
    all_column4_df = pd.DataFrame()

    for file_pattern, sheet_name in zip(file_patterns, sheet_names):
        # Initialize empty DataFrames for each sheet
        column3_df = pd.DataFrame()
        column4_df = pd.DataFrame()
        file_names = []

        # Loop through matching files
        for file in sorted(glob(file_pattern)):  # Sorted to maintain order
            # Extract the base name
            base_name = os.path.splitext(file)[0]

            # Extract the third and fourth columns starting from the second row
            data_df = pd.read_table(file, sep='\s+', skiprows=1, usecols=[2, 3], header=None, names=['Shielding', 'Chemical_Shift'])

            # Concatenate the columns horizontally
            column3_df = pd.concat([column3_df, data_df['Shielding']], axis=1)
            column4_df = pd.concat([column4_df, data_df['Chemical_Shift']], axis=1)
            file_names.append(base_name)

        # Save the extracted data to an Excel file for each sheet
        column3_df.columns = file_names
        column4_df.columns = file_names
        column3_df.to_excel(writer, sheet_name=f'{sheet_name}_Shielding', index=False, startrow=1)
        column4_df.to_excel(writer, sheet_name=f'{sheet_name}_Chemical_Shift', index=False, startrow=1)

        # Concatenate the columns horizontally for the consolidated sheet
        all_column3_df = pd.concat([all_column3_df, column3_df], axis=1)
        all_column4_df = pd.concat([all_column4_df, column4_df], axis=1)

    # Save the consolidated data to an Excel file
    all_column3_df.to_excel(writer, sheet_name=f'Consolidated_Shielding', index=False)
    all_column4_df.to_excel(writer, sheet_name=f'Consolidated_Chemical_Shift', index=False)

# Save the extracted data to an Excel file
excel_file = 'extracted_data_combined_with_names.xlsx'
with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    file_patterns = ['*_09_CWeighted01.txt', '*_09_HWeighted01.txt', '*_09_CWeighted02.txt', '*_09_HWeighted02.txt', '*_09_CWeighted03.txt', '*_09_HWeighted03.txt']
    sheet_names = ['CWeighted01', 'HWeighted01', 'CWeighted02', 'HWeighted02', 'CWeighted03', 'HWeighted03']
    extract_and_concatenate(file_patterns, sheet_names, writer)

print(f'Extracted data with file names saved to {excel_file}')
