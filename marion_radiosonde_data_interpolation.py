###This python script reads multiple csv files of "Maturilli, Marion: High resolution radiosonde measurements from station Ny-Ålesund. Alfred Wegener Institute - Research Unit Potsdam, PANGAEA" and linearly interpolated the variables. 
###TIME and ETIM were not interpolated instead placed the nearest values corresponding to the Altitude values.
###The origional Radiosonde data is in ".tab" format and converted to ".csv" format. I have used <marion_radiosonde_data_tab_to_csv.py> script for the conversion.
###Linear Interpolation done at each meter from 17 to 10000m.



import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import os

folder_path = '.'
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

for input_file in csv_files:
    file_name_without_ext = os.path.splitext(input_file)[0]

    df = pd.read_csv(os.path.join(folder_path, input_file))
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    grouped = df.groupby(df['DateTime'].dt.date)

    min_height = df['Altitude'].min()
    max_height = df['Altitude'].max()

    output_min_height = max(min_height, 17)
    output_max_height = min(max_height, 10000)
    output_heights = np.arange(output_min_height, output_max_height + 1, 1)

    output_data = pd.DataFrame(columns=['Time', 'Latitude', 'Longitude', 'Height (m)', 'Pressure (hPa)',
                                        'Temperature (degC)', 'Relative Humidity (%)', 'Wind Direction (deg)',
                                        'Wind Speed (m/s)', 'ETIM', 'HGEOM'])

    for date, group in grouped:
        valid_mask = pd.to_numeric(group['Altitude'], errors='coerce').notnull()

        time = group.loc[valid_mask, 'DateTime']
        height = group.loc[valid_mask, 'Altitude']

        pressure = group.loc[valid_mask, 'PPPP']
        temperature = group.loc[valid_mask, 'TTT']
        relhumidity = group.loc[valid_mask, 'RH']
        winddir = group.loc[valid_mask, 'DD']
        windspeed = group.loc[valid_mask, 'FF']
        latitude = group.loc[valid_mask, 'Lat']
        longitude = group.loc[valid_mask, 'Lon']
        etim = group.loc[valid_mask, 'ETIM']
        hgeom = group.loc[valid_mask, 'HGEOM']


        interp_func_pressure = interp1d(height, pressure, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_pressure = interp_func_pressure(output_heights)
        interpolated_pressure = np.round(interpolated_pressure, decimals=2)

        interp_func_temperature = interp1d(height, temperature, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_temperature = interp_func_temperature(output_heights)
        interpolated_temperature = np.round(interpolated_temperature, decimals=2)

        interp_func_relhumidity = interp1d(height, relhumidity, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_relhumidity = interp_func_relhumidity(output_heights)
        interpolated_relhumidity = np.round(interpolated_relhumidity, decimals=2)

        interp_func_winddir = interp1d(height, winddir, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_winddir = interp_func_winddir(output_heights)
        interpolated_winddir = np.round(interpolated_winddir, decimals=2)

        interp_func_windspeed = interp1d(height, windspeed, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_windspeed = interp_func_windspeed(output_heights)
        interpolated_windspeed = np.round(interpolated_windspeed, decimals=2)

        interp_func_hgeom = interp1d(height, hgeom, kind='linear', fill_value=np.nan, bounds_error=False)
        interpolated_hgeom = interp_func_hgeom(output_heights)
        interpolated_hgeom = np.round(interpolated_hgeom, decimals=2)

        nearest_indices = np.abs(height.values[:, np.newaxis] - output_heights).argmin(axis=0)
        nearest_etim = etim.iloc[nearest_indices].reset_index(drop=True)

        nearest_indices = np.abs(height.values[:, np.newaxis] - output_heights).argmin(axis=0)
        nearest_times = time.iloc[nearest_indices].reset_index(drop=True)

        latitude = latitude.iloc[nearest_indices].reset_index(drop=True)
        longitude = longitude.iloc[nearest_indices].reset_index(drop=True)

        group_output_data = pd.DataFrame({
    					'Time': nearest_times,
				        'Latitude': latitude,
					'Longitude': longitude,
					'Height (m)': output_heights,
					'Pressure (hPa)': interpolated_pressure,
					'Temperature (degC)': interpolated_temperature,
					'Relative Humidity (%)': interpolated_relhumidity,
					'Wind Direction (deg)': interpolated_winddir,
					'Wind Speed (m/s)': interpolated_windspeed,
					'ETIM': nearest_etim,
					'HGEOM': interpolated_hgeom
	})
        output_data = pd.concat([output_data, group_output_data], ignore_index=True)

    output_file = os.path.join(folder_path, file_name_without_ext + "_interpolated.csv")
    output_data.to_csv(output_file, index=False)

    print(output_data)
    print("Interpolated data saved to", output_file)
