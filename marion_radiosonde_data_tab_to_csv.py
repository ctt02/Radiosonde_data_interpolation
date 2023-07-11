###This script reads multiple .tab data files of "Maturilli, Marion: High resolution radiosonde measurements from station Ny-Ålesund. Alfred Wegener Institute - Research Unit Potsdam, PANGAEA" and converts to ".csv" format.
###Outputs created from this script is used to linearly interpolate the data at each level.



import pandas as pd
from pathlib import Path

def convert_tab_to_csv(tab_file, headers):
    parsed_lines = []

    try:
        with open(tab_file, 'r') as file:
            for i, line in enumerate(file):
                if i < 23:
                    continue
                try:
                    parsed_line = line.strip().split('\t')
                    if len(parsed_line) < 2:
                        continue  # Skip lines that do not have enough values

                    # Convert DateTime format
                    date_time = parsed_line[0].split('T')[0]
                    time = parsed_line[0].split('T')[1]
                    parsed_line[0] = f"{date_time.replace('-', '/')} {time}"
                    parsed_lines.append(parsed_line)
                except (IndexError, ValueError):
                    continue  # Skip lines that cannot be parsed

    except FileNotFoundError:
        print(f"File {tab_file} not found")

    if parsed_lines:
        csv_file = Path(tab_file).with_suffix('.csv')
        empty_df = pd.DataFrame(parsed_lines, columns=headers)
        empty_df = empty_df.iloc[1:]
        empty_df.to_csv(csv_file, index=False)
        print(f"Converted {tab_file} to {csv_file}")
directory_path = Path('.')

tab_files = directory_path.glob('*.tab')

headers = ['DateTime', 'Lat', 'Lon', 'Altitude', 'HGEOM', 'ETIM', 'PPPP', 'TTT', 'RH', 'DD', 'FF']

for tab_file in tab_files:
    convert_tab_to_csv(tab_file, headers)
