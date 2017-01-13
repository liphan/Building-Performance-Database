#!/usr/bin/python

from os import listdir
import csv
import pandas as pd

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

csv_files_array = find_csv_filenames("/Users/LipHan/dat2/Building-Performance-Database")

#Empty datafram
final_df = pd.DataFrame(columns=['count','percentile_0','facility_type','floor_area_min','floor_area_max','percentile_50','standard_dev','percentile_25','percentile_75','percentile_100','mean','state'])

for file in csv_files_array:
	df = pd.read_csv(file, index_col=None)
	state = file.split('_')[0]
	df['state'] = state
	final_df = final_df.append(df, ignore_index = True)

print(final_df.head())
#Write to csv
final_df.to_csv('combine_states.csv', index=False)
