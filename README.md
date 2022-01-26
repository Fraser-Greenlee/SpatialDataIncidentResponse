# Spatial Data for Incident Response (Cave Rescue)

**Rationale**

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations in addition to locating specific team members best positioned to respond. This provides the opportunity to accurately record these locations and other useful information in advance of incidents occurring and make them readily accessible. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs), and team member locations.

\
**Contents**

The follow scripts use data available only for mainland GB from the Ordnance Survey, therefore areas outside mainland GB are unsupported.

```AugmentLocations.py```:
- ingests APs and RVs recorded in spreadsheets (spreadsheet and QGIS mapping templates are provided)
- adds accurate spatial conversions from longitude and latitude coordinates to:
  - British National Grid easting and northing
  - Ordnance Survey 1m grid reference
  - What3Words address
  - Google Maps URL (cross-platform app integration)
- and metadata:
  - road access type
  - nearest postcode
  - mobile phone coverage for all providers
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx)

```GeolocateAddresses.py```:
- ingests team member addresses recorded in a spreadsheet (a spreadsheet template is provided)
- extracts postcodes from the addresses
- adds longitude and latitude coordinates using the postcode, resulting in an approximate location
- exports this information in a variety of useful formats (.csv, .gpkg)

\
**Templates**

- ```Mapping.qgz``` - [QGIS](https://qgis.org/en/site/) project containing various web map services for remote mapping
- ```APs_Master.ods``` - spreadsheet for recording APs
- ```RVs_Master.ods``` - spreadsheet for recording RVs
- ```TeamMembers_Master.ods``` - spreadsheet for recording team member addresses

\
**Setup**

Each Python script contains essential setup instructions that are required prior to use to ensure accuracy and correct function.
