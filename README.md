# Spatial Data for Incident Response (Cave Rescue)



# Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations. This provides the opportunity to accurately record these locations and make them readily accessible in advance of incidents occurring, allowing incident controllers access to detailed location information ready for rapid and error-free sharing with team members and other emergency services. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs).



# Methodology
- use ```Mapping.qgz``` ([QGIS](https://qgis.org/en/site/) project containing various web map services for remote location mapping) to generate WGS84 longitude, latitude coordinates for each location and paste them into a spreadsheet template (```APs_Master.ods``` or ```RVs_Master.ods```) depending on the location type, adding additional information and columns as required (these will be unaltered and will carry through)

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Coordinates.png" height="300">

- use ```AugmentLocations.py``` to automatically add conversions and metadata to the spreadsheet records, and export the data in useful formats
- serve the exported files according to your requirements



# Data Serving
Below are free and open source methods of serving the data that also allow the interrogation of location metadata.

**Google Maps**
- uses .csv files for upload
- online access (user permissions for privacy)
  
  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Google.png" height="300">


**QGIS**
- can ingest any spatial data format
- local PC only
  
  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/QGIS.png" height="300">


**Mobile Device**
- uses .gpx files for import
- offline navigation and data access
  
  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Mobile.png" height="300">



# AugmentLocations.py
```AugmentLocations.py``` uses data available only for mainland Great Britain, therefore areas outside mainland Great Britain are unsupported.

**Dependencies:** Numpy, Pandas, GeoPandas, GPXpy, ODF

**Function:**
- ingests APs and RVs recorded in spreadsheets
- adds spatial conversions and metadata using the WGS84 longitude, latitude coordinates

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Augment.png" height="500">
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx)
