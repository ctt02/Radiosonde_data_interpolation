


import os
import glob
import pandas as pd

input_files = glob.glob("*_selected.csv")

dfs = []

for input_file_path in input_files:
    df = pd.read_csv(input_file_path)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

combined_df.sort_values('Time', inplace=True)

variables = combined_df.columns[4:]

combined_output_file_path = os.path.join(os.getcwd(), "combined_input.csv")
combined_df.to_csv(combined_output_file_path, index=False)
print(f"Combined input file saved successfully as '{combined_output_file_path}'.")

for variable in variables:
    output_df = combined_df.pivot_table(index='Time', columns='Height (m)', values=variable)

    output_df.columns = output_df.columns.astype(str)

    # Get a simple variable name without any spaces or special characters
    variable_name = variable.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
    output_filename = f"output_combined_{variable_name}.csv"
    output_file_path = os.path.join(os.getcwd(), output_filename)

    output_df.to_csv(output_file_path, index_label='Time')
    print(f"CSV file for variable '{variable}' saved successfully as '{output_file_path}'.")

print("All CSV files processed and saved successfully.")
