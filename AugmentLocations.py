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
    The purpose of this software is to ingest spreadsheets containing spatial
    records of cave and mine Access Points (APs) and Rendezvous points (RVs),
    to accurately and automatically convert these into a variety of location
    formats, and add useful metadata from free external datasets and services.
    The data are exported in a variety of standard formats.

Column list:
    Required in spreadsheet (additional columns are unaltered):
        Name - Location name
        ID - Unique identifier
        VerifiedDate - Date of visit to verify location
        Longitude - Decimal degrees (WGS84)
        Latitude - Decimal degrees (WGS84)
    Generated for RVs only:
        RoadAccessType - Nearest road type
        Postcode - Nearest postcode
        MobileCoverage - Minimum outdoor mobile phone coverage
    Generated for all locations:
        Verified - Binary flag if checked
        Easting - Metres (British National Grid)
        Northing - Metres (British National Grid)
        OSGridRef1m - Ordnance Survey 1m grid reference
        What3Words - What3Words address
        GoogleMapsURL - Google Maps link for directions and Street View

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
        
    2. Download files and register for API keys:
        - OS GB Postcode data - https://osdatahub.os.uk/downloads/open/CodePointOpen
        - OS GB Road data - https://osdatahub.os.uk/downloads/open/OpenRoads
        - Ofcom Mobile API - https://api.ofcom.org.uk/products/mobile-premium
        - What3Words API - https://developer.what3words.com/public-api
        
    3. Edit the user-defined variables to point to the required locations and
    include your API keys
"""



# User-defined variables
ap_filepath = "/APs_Master.ods" # APs spreadsheet filepath
rv_filepath = "/RVs_Master.ods" # RVs spreadsheet filepath
codepoint_filepath = "/codepo_gb.gpkg" # Code Point filepath
openroads_filepath = "/oproad_gb.gpkg" # Open Roads filepath
export_directory = "/Processed" # Any directory to export the processed files to
ofcom_api_key = '#####' # Paste your API key here
what3words_api_key = '#####' # Paste your API key here
rv_gpx_symbology = 'None' # Optional - Replace with the symbology text string that is unique to the GPS device
ap_gpx_symbology = 'None'# Optional - Replace with the symbology text string that is unique to the GPS device



import os
import time
import http.client
import urllib.parse
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import gpxpy
import gpxpy.gpx as g
from datetime import datetime
from scipy.spatial import cKDTree
from shapely.ops import cascaded_union
from shapely.geometry import LineString



def get_coverage(postcode):
    key = ofcom_api_key
    api_url_root = "api-proxy.ofcom.org.uk"
    fixed_url = "/mobile/coverage/"
    params = urllib.parse.urlencode({})
    headers = {"Ocp-Apim-Subscription-Key": key}
    try:
        conn = http.client.HTTPSConnection(api_url_root)
        conn.request('GET', fixed_url + postcode + "?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        if 'Error' in data.keys():
            raise Exception
        return [address for address in data['Availability']]
    except:
        return None

def get_what3words(lat, long):
    key = what3words_api_key
    api_url_root = "api.what3words.com"
    fixed_url = "/v3/convert-to-3wa?coordinates="
    try:
        conn = http.client.HTTPSConnection(api_url_root)
        conn.request('GET', fixed_url + str(lat) + "%2C" + str(long) + "&key=" + key)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return data['words']
    except:
        return None

def point_buffer(points, distance, crs):
    buffer = points.buffer(distance)
    return gpd.GeoSeries(cascaded_union(buffer), crs = crs)

def get_nearest(gdA, gdB):
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k = 1)
    gdB_nearest = gdB.iloc[idx].drop(columns = 'geometry').reset_index(drop = True)
    gdf = pd.concat([gdA.reset_index(drop = True),
                     gdB_nearest,
                     pd.Series(dist, name = 'dist')], axis = 1)
    return gdf

def redistribute_vertices(geom, distance):
    if geom.geom_type == 'LineString':
        num_vert = int(round(geom.length/distance))
        if num_vert == 0:
            num_vert = 1
        return LineString([geom.interpolate(float(n)/num_vert, normalized = True) for n in range(num_vert + 1)])
    elif geom.geom_type == 'MultiLineString':
        parts = [redistribute_vertices(part, distance) for part in geom]
        return type(geom)([p for p in parts if not p.is_empty])
    else:
        raise ValueError("Unhandled geometry %s", (geom.geom_type))

def xy_to_osgb(easting, northing, precision = 1):
    major = {0: {0: 'S', 1: 'N', 2: 'H'},
             1: {0: 'T', 1: 'O'}}
    minor = {0: {0: 'V', 1: 'Q', 2: 'L', 3: 'F', 4: 'A'},
             1: {0: 'W', 1: 'R', 2: 'M', 3: 'G', 4: 'B'},
             2: {0: 'X', 1: 'S', 2: 'N', 3: 'H', 4: 'C'},
             3: {0: 'Y', 1: 'T', 2: 'O', 3: 'J', 4: 'D'},
             4: {0: 'Z', 1: 'U', 2: 'P', 3: 'K', 4: 'E'}}
    
    if precision not in [100000, 10000, 1000, 100, 10, 1]:
        raise Exception('Precision of', str(precision), 'is not supported')
    
    try:
        x_idx = easting // 500000
        y_idx = northing // 500000
        major_letter = major[x_idx][y_idx]
        macro_easting = easting % 500000
        macro_northing = northing % 500000
        macro_x_idx = macro_easting // 100000
        macro_y_idx = macro_northing // 100000
        minor_letter = minor[macro_x_idx][macro_y_idx]
    except (ValueError, IndexError, KeyError, AssertionError):
        raise Exception('Out of range')
    
    micro_easting = macro_easting % 100000
    micro_northing = macro_northing % 100000
    ref_x = micro_easting // precision
    ref_y = micro_northing // precision

    coord_width = 0
    if precision == 10000:
        coord_width = 1
    elif precision == 1000:
        coord_width = 2
    if precision == 100:
        coord_width = 3
    elif precision == 10:
        coord_width = 4
    elif precision == 1:
        coord_width = 5

    format_string = (r"%s%s %0" + str(coord_width) + r"d %0" +
                     str(coord_width) + r"d") if precision else r"%s%s %0"
    return format_string % (major_letter, minor_letter, ref_x, ref_y)



# Check that all filepaths and directories exist
for path in [ap_filepath, rv_filepath, codepoint_filepath,
             openroads_filepath, export_directory]:
    if not os.path.exists(path):
        raise Exception('Path ' + str(path) + ' does not exist')


        
# Timestamp
date = datetime.now().strftime("%Y-%m-%d")

# Loop through each location type and spreadsheet
for location_type, path in zip(['APs', 'RVs'], [ap_filepath, rv_filepath]):
    
    print('Processing', location_type)
    
    # Read in the master spreadsheet
    data = pd.read_excel(path, engine = 'odf')
    
    
    
    print(" - Formatting Inputs")
    # Check for blanks in essential columns
    for i in ['ID', 'Name', 'Longitude', 'Latitude']:
        if data[i].isna().sum() > 0:
            raise Exception(i + ' contains blank values')
    
    # Set column data types
    try:
        for i in ['Name', 'ID']:
            data[i] = data[i].astype(str)
    except:
        raise Exception(i + ' contains non-string values')
    try:
        for i in ['VerifiedDate']:
            data[i] = pd.to_datetime(data[i])
    except:
        raise Exception(i + ' contains non-datetime values')
    try:
        for i in ['Longitude', 'Latitude']:
            data[i] = data[i].astype(float)
    except:
        raise Exception(i + ' contains non-numeric values')
    
    # Check for duplicate IDs
    if len(data['ID']) != len(set(data['ID'])):
        raise Exception('IDs are not unique')
        
    # Concatenate the name and ID columns, removing the latter
    data['Name'] = data['Name'].astype(str) + " (" + data.pop('ID').astype(str) + ")"
    
    
    
    print(" - Creating Backup")
    # Export a timestamped CSV backup to the spreadsheet directory
    data.to_csv(os.path.join(os.path.dirname(path),
                             location_type + "_Backup_" + date + ".csv"),
                index = False)



    print(" - Adding Geometry")
    # Add geometry, set as WGS84
    data = gpd.GeoDataFrame(data,
                            crs = "EPSG:4326",
                            geometry = gpd.points_from_xy(data['Longitude'],
                                                          data['Latitude']))
    # Convert to BNG
    data = data.to_crs("EPSG:27700")
    
    
    
    print(" - Handling Dates")
    # Convert dates to datetime
    data['VerifiedDate'] = pd.to_datetime(data['VerifiedDate'], errors = 'coerse')
    # If there is a valid date, create a binary flag
    data['Verified'] = 'False'
    data.loc[data['VerifiedDate'].notnull(), 'Verified'] = 'True'
    # Get date from datetime
    data['VerifiedDate'] = data.pop('VerifiedDate').dt.strftime("%Y-%m-%d")
    
    
    
    if location_type == 'RVs':
        
        print(" - Road Access Type")
        # Read in Open Roads data within a distance of each RV as BNG
        road_dist = 50
        roads = gpd.read_file(openroads_filepath,
                              mask = point_buffer(data, road_dist, "EPSG:27700"))
        roads.crs = "EPSG:27700"
        # Keep only necessary columns
        roads = roads[['roadFunction', 'geometry']]
        
        # Clip roads to the buffer and convert to single part
        roads = gpd.clip(roads, point_buffer(data, road_dist, "EPSG:27700")).explode()
        # Resample the road vertices
        roads['geometry'] = roads.geometry.apply(redistribute_vertices, distance = 2)
        
        # Extract the coordinates of each vertex for each line as points with their road access type
        road_type_points = gpd.GeoDataFrame(crs = "EPSG:27700")
        for index, row in roads.iterrows():
            coords = [i for i in row['geometry'].coords]
            temp = gpd.GeoDataFrame(crs = "EPSG:27700",
                                    geometry = gpd.points_from_xy([x for x, y in coords],
                                                                  [y for x, y in coords]))
            temp['RoadAccessType'] = row['roadFunction']
            road_type_points = road_type_points.append(temp)
            
        # Get the closest road type point and distance in metres
        data = get_nearest(data, road_type_points)
        data['RoadDistanceMetres'] = data.pop('dist').round(0).astype(int)
        # Remove roads further than the buffer distance
        data.loc[data['RoadDistanceMetres'] > road_dist, 'RoadAccessType'] = 'Unknown'
        # Remove the distance column
        del data['RoadDistanceMetres']
        
        
        
        print(" - Postcode")
        # Read in Code Point data within a distance of each RV as BNG
        postcode_dist = 300
        postcodes = gpd.read_file(codepoint_filepath,
                                  mask = point_buffer(data, postcode_dist, "EPSG:27700"))
        postcodes.crs = "EPSG:27700"
        # Keep only necessary columns
        postcodes = postcodes[['Postcode', 'geometry']]
        # Remove spaces
        postcodes['Postcode'] = postcodes['Postcode'].str.replace(' ', '')
        # Get the closest postcode and distance in metres
        data = get_nearest(data, postcodes)
        data['PostcodeDistanceMetres'] = data.pop('dist').round(0).astype(int)
        # Remove postcodes further than the buffer distance
        data.loc[data['PostcodeDistanceMetres'] > postcode_dist, 'Postcode'] = 'None'
        # Remove the distance column
        del data['PostcodeDistanceMetres']
        
        
        
        print(" - Mobile Phone Coverage")
        # All providers
        providers = {'EE': 'EE',
                     'H3': 'Three',
                     'VO': 'Vodafone',
                     'TF': 'O2'}
        # Scores and meaning
        coverage_scores = {0: 'Black',  # No signal predicted
                           1: 'Red',    # Reliable signal unlikely
                           2: 'Amber',  # May experience problems with connectivity
                           3: 'Green',  # Likely to have good coverage and receive a basic data rate
                           4: 'Blue'}   # Likely to have good coverage indoors and to receive an enhanced data rate
        
        # Create the postcode-coverage lookup
        mobile_coverage = {}
        for postcode in list(set(data['Postcode'])):
            time.sleep(0.15) # < 500 calls/minute limit
            coverage = get_coverage(postcode)
            # If we get results back
            if coverage:
                provider_results = []
                # Get the lowest score for each provider in the postcode for outdoor voice calls without 4G
                for provider in providers.keys():
                    provider_name = providers.get(provider)
                    score = min([i.get(provider + 'VoiceOutdoorNo4g') for i in coverage])
                    # Check that the returned score is valid
                    if score not in coverage_scores.keys():
                        raise Exception('Coverage score ' + str(score) + ' is not valid')
                    # Format the provider result and add it to the list
                    provider_results.append(provider_name + " (" + coverage_scores.get(score) + ")")
                # Concatenate the provider results and assign to the postcode
                mobile_coverage[postcode] = ", ".join(provider_results)
            # If we don't get results back
            else:
                mobile_coverage[postcode] = 'Unknown'
                
        # Lookup the coverage for each postcode
        data['MobileCoverage'] = [mobile_coverage.get(i) for i in data['Postcode']]
    
    
    
    # Regardless of location type
    
    print(" - Longitude, Latitude")
    data['Longitude'] = data.pop('Longitude')
    data['Latitude'] = data.pop('Latitude')
    
    print(" - Easting, Northing")
    data['Easting'] = data['geometry'].x.astype(int)
    data['Northing'] = data['geometry'].y.astype(int)

    print(" - OS Grid Reference")
    data['OSGridRef1m'] = data.apply(lambda x: xy_to_osgb(x['geometry'].x, x['geometry'].y), axis = 1)

    print(" - What3Words")
    data['What3Words'] = data.apply(lambda x: get_what3words(x['Latitude'], x['Longitude']), axis = 1)
    
    print(" - Google Maps URL")
    # https://developers.google.com/maps/documentation/urls/get-started
    data['GoogleMapsURL'] = "https://www.google.com/maps/search/?api=1&query=" + data['Latitude'].astype(str) + "%2C" + data['Longitude'].astype(str)
    
    
    
    print(" - Exporting Files")
    # Replace blanks with none
    data = data.replace(np.nan, 'None').replace('NaT', 'None')
    
    # Reset index and name as fid
    data = data.reset_index(drop = True)
    data.index.name = 'fid'
    # Start the index at 1
    data.index += 1 
    
    # Export to BNG GeoPackage
    data.to_file(os.path.join(export_directory,
                              location_type + "_BNG.gpkg"),
                 layer = location_type + "_BNG",
                 driver = 'GPKG')
    
    # Convert to WGS84 using the original longitude and latitude
    data = gpd.GeoDataFrame(data,
                            crs = "EPSG:4326",
                            geometry = gpd.points_from_xy(data['Longitude'],
                                                          data['Latitude']))
    
    # Export to WGS84 GeoPackage
    data.to_file(os.path.join(export_directory,
                              location_type + "_WGS84.gpkg"),
                 layer = location_type + "_WGS84",
                 driver = 'GPKG')
    
    # Remove the geometry column
    del data['geometry']
    
    # Export to CSV
    data.to_csv(os.path.join(export_directory,
                             location_type + ".csv"),
                index = False)
    
    

    # Build a GPX file
    # Loop through each row and concatenate columns
    descriptions = []
    for i, row in data.iterrows():
        descriptions.append(" | ".join([str(row.index.values[i]) + ": " + str(row.values[i]) for i in range(len(row.index.values))]))
    data['Concat'] = descriptions
    
    # Create a blank GPX file
    gpx = g.GPX()
    gpx.creator = "AugmentLocations.py -- github.com/EdwardALockhart/SpatialDataIncidentResponse"
    
    # Loop through each location record
    for i, row in data.iterrows():
        # Create a blank waypoint
        wpt = gpxpy.gpx.GPXWaypoint()
        
        # Add data to the waypoint
        wpt.name = row['Name']
        wpt.longitude = row['Longitude']
        wpt.latitude = row['Latitude']
        wpt.comment = row['Concat']
        wpt.desciption = row['Concat']
        if location_type == 'RVs' and rv_gpx_symbology != 'None':
            wpt.symbol = rv_gpx_symbology
        elif location_type == 'APs' and ap_gpx_symbology != 'None':
            wpt.symbol = ap_gpx_symbology
            
        # Add to the GPX file
        gpx.waypoints.append(wpt)
    
    # Export to WGS84 GPX
    with open(os.path.join(export_directory,
                           location_type + "_" + date + "_WGS84.gpx"),
              'w') as file:
        file.write(gpx.to_xml(version = "1.1"))

    print(" - Done\n")



print('Complete')
