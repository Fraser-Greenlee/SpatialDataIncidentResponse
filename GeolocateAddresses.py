"""
Copyright (C) Edward Alan Lockhart 2022

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see https://www.gnu.org/licenses/.

Description:
    The purpose of this software is to ingest a spreadsheet of team member
    addresses and geolocate them as coordinates of longitude and latitude
    using extracted postcodes.

Column list:
    Required in spreadsheet (additional columns will be concatenated):
        Name - Team member name
        Address - Team member address with postcode

Setup:    
    1. To ensure the most accurate conversion between longitude and latitude
    and British National Grid, the OSTN15-NTv2 transformation is required. To
    check if this is installed, run:

        import pyproj
        tg = pyproj.transformer.TransformerGroup(27700, 4326)
        descriptions = "\n\n".join([str(i) for i in tg.transformers])
        if "OSTN15_NTv2" in descriptions:
            print("OSTN15_NTv2 is present")
        else:
            print("OSTN15_NTv2 is not present")

    If OSTN15_NTv2 is not present, download and extract the files in
    https://ordnancesurvey.co.uk/documents/resources/OSTN15-NTv2.zip to the
    directory produced by:

        import pyproj
        print(pyproj.datadir.get_data_dir())

    2. Download files:
        - OS GB Postcode data - https://osdatahub.os.uk/downloads/open/CodePointOpen
        
    3. Edit the user-defined variables to point to the required locations
"""



# User-defined variables
teammembers_filepath = "/TeamMembers_Master.ods" # Team members spreadsheet filepath
codepoint_filepath = "/codepo_gb.gpkg" # CodePoint filepath
export_directory = "/Processed" # Any directory to export the processed files to



import os
import re
import pandas as pd
import geopandas as gpd
from datetime import datetime



def find_postcode(address):
    # https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes
    search = re.findall(r"(([A-Z]{1,2}\d[A-Z\d]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?\d[A-Z]{2}|BFPO ?\d{1,4}|(KY\d|MSR|VG|AI)[ -]?\d{4}|[A-Z]{2} ?\d{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)", address)
    if search:
        return search[-1][0].upper().replace(' ', '')
    else:
        return 'None'



# Check that all filepaths and directories exist
for path in [teammembers_filepath, codepoint_filepath, export_directory]:
    if not os.path.exists(path):
        raise Exception('Path ' + str(path) + ' does not exist')



print('Processing Team Members')

# Timestamp
date = datetime.now().strftime("%Y-%m-%d")

# Read in the team members spreadsheet
data = pd.read_excel(teammembers_filepath, engine = 'odf')



print(" - Formatting Inputs")
# Check for blanks in essential columns
for i in ['Name', 'Address']:
    if data[i].isna().sum() > 0:
        raise Exception(i + ' contains blank values')

# Set column data types
try:
    for i in ['Name', 'Address']:
        data[i] = data[i].astype(str)
except:
    raise Exception(i + ' contains non-string values')



print(" - Creating Backup")
# Export a timestamped CSV backup to the spreadsheet directory
data.to_csv(os.path.join(os.path.dirname(teammembers_filepath),
                         "TeamMembers_Backup_" + date + ".csv"),
            index = False)


    
print(" - Extracting Postcodes and Joining Columns")
# Extract postcodes from the address column
data['Postcode'] = data.apply(lambda x: find_postcode(x['Address'].upper()), axis = 1)
# Remove the address column
del data['Address']

# Prefix values with colum names and then concatenate the columns
cols = [i for i in data.columns if i not in ['Name', 'Postcode']]
for col in cols:
    data[col] = col + ": " + data[col].astype(str)
data['Concat'] = data[cols].apply(lambda row: " | ".join(row.values.astype(str)), axis = 1)
# Remove the original columns
data = data.drop(cols, axis = 1)

# Join the name and concatenated columns
data['Info'] = data.pop('Name').astype(str) + " (" + data.pop('Concat').astype(str) + ")"



print(" - Reading OS CodePoint Data")
# Read in OS CodePoint data
postcodes = gpd.read_file(codepoint_filepath)
postcodes.crs = "EPSG:27700"
postcodes = postcodes[['Postcode', 'geometry']]

# Remove spaces
postcodes['Postcode'] = postcodes['Postcode'].str.replace(' ', '')

# Isolate postcodes
postcodes = postcodes.loc[postcodes['Postcode'].isin(set(data['Postcode']))]



print(" - Joining Datasets")
# Join on postcode
data = pd.merge(data, postcodes, on = 'Postcode', how = 'left')

# Concatenate instances if they use the same postcode
data['Info'] = data.groupby(['Postcode'])['Info'].transform(lambda x: "\n".join(x))

# Remove the postcode column
del data['Postcode']

# Remove any duplicates
data = data.drop_duplicates()



print(" - Exporting Files")
# Read as BNG
data = gpd.GeoDataFrame(data,
                        crs = "EPSG:27700",
                        geometry = 'geometry')

# Reset index and name as fid
data = data.reset_index(drop = True)
data.index.name = 'fid'
# Start the index at 1
data.index += 1 

# Export to BNG GeoPackage
data.to_file(os.path.join(export_directory,
                          "TeamMembers_BNG.gpkg"),
             layer = "TeamMembers_BNG",
             driver = 'GPKG')

# Convert to WGS84
data = data.to_crs("EPSG:4326")

# Export to WGS84 GeoPackage
data.to_file(os.path.join(export_directory,
                          "TeamMembers_WGS84.gpkg"),
             layer = "TeamMembers_WGS84",
             driver = 'GPKG')

# Extract coordinates
data['Longitude'] = data['geometry'].x
data['Latitude'] = data['geometry'].y

# Remove the geometry column
del data['geometry']

# Export to CSV
data.to_csv(os.path.join(export_directory,
                         "TeamMembers.csv"),
            index = False)



print('Complete')
