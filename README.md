# Spatial Data for Incident Response (Cave Rescue)



### Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations. This provides the opportunity to accurately record these locations and make them readily accessible in advance of incidents occurring, allowing incident controllers access to detailed location information ready for rapid and error-free sharing with team members and other emergency services. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs).



### Methodology
- download and open [```Mapping.qgz```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/Mapping.qgz), a [QGIS](https://qgis.org/en/site/) project containing various web map services for remote location mapping. Generate WGS84 longitude, latitude coordinates for each location and paste them into a spreadsheet template ([```APs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/APs_Master.ods) or [```RVs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/RVs_Master.ods)) depending on the location type, adding additional information and columns as required (these will be unaltered and will carry through)

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Coordinates.png" height="300">
  
  _Extracting coordinates for a location using right-click with the hand tool selected in QGIS_

- visit [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) and follow the instructions to automatically add spatial conversions and metadata to the spreadsheet records, and export the data in useful formats
- serve the exported files according to your requirements



### [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb)
[```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) is created for use with [Google Colaboratory](https://colab.research.google.com/) - everything runs temporarily in the cloud, so no setup is required on your local PC which is best for those with no technical coding experience. It runs in a web browser and accesses files hosted on your Google Drive for persistent storage between sessions, and therefore requires a free Google account. The code can also be used on a local PC with a python installation, [Anaconda](https://www.anaconda.com/) is recommended.

The code uses data available only for mainland Great Britain, therefore areas outside mainland Great Britain are unsupported.

**Function:**
- ingests APs and RVs recorded in spreadsheets
- adds spatial conversions
    - Postcode - Nearest postcode
    - Longitude - Decimal degrees (WGS84)
    - Latitude - Decimal degrees (WGS84)
    - Easting - Metres (British National Grid)
    - Northing - Metres (British National Grid)
    - OSGridRef1m - Ordnance Survey 1m grid reference
    - What3Words - What3Words address
    - GoogleMapsURL - Google Maps link for directions and Street View
- and metadata
    - RoadAccessType - Nearest road type
    - MobileCoverage - Minimum outdoor mobile phone coverage

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Augment.png" height="500">
- exports this information in a variety of useful formats (.csv, .gpkg, .gpx)



### Data Serving
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
