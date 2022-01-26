# Spatial Data for Incident Response (Cave Rescue)

**Rationale**

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations in addition to locating specific team members. This provides the opportunity to accurately record these locations and other useful information in advance of incidents occurring. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs), and team member locations.
\
\
This GitHub repository contains ```AugmentLocations.py```, which:
- adds accurate spatial conversions and metadata to APs and RVs recorded in spreadsheets (spreadsheet and QGIS mapping templates are provided)
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx) and coordinate systems (WGS84, British National Grid)

and ```GeolocateAddresses.py```, which:
- extracts postcodes from team member addresses recorded in a spreadsheet (a spreadsheet template is provided)
- adds longitude and latitude coordinates using the postcodes, resulting in an approximate location
- exports this information in a variety of useful formats (.csv, .gpkg) and coordinate systems (WGS84, British National Grid)

\
**Templates**

- **Mapping.qgz** - [QGIS](https://qgis.org/en/site/) project containing various web map services for remote mapping
- **APs_Master.ods** - Spreadsheet for recording APs
- **RVs_Master.ods** - Spreadsheet for recording RVs
- **TeamMembers_Master.ods** - Spreadsheet for recording team member addresses

\
**Setup**

East Python script contains essential setup instructions that are required prior to use to ensure accuracy and correct function.
