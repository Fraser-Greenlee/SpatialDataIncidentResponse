# Spatial Data for Incident Response (Cave Rescue)



### Rationale

Cave Rescue teams have a unique use case regarding spatial data, specifically the need to rapidly share and navigate to often predetermined and precise incident locations. This provides the opportunity to accurately record these locations and make them readily accessible in advance of incidents occurring, allowing incident controllers access to detailed location information ready for rapid and error-free sharing with team members and other emergency services. These locations comprise of cave and mine Access Points (APs) and Rendezvous points (RVs).

The methodology below describes how to:
- collect - collate location data from various sources into a structured format based on longitude and latitude
- augment - add accurate spatial conversions and metadata to each location
- serve - make the augmented locations accessible

A spatial catalogue of APs and RVs helps with identifing all possible underground locations in an area and what RVs are best positioned for the task at hand. Having accurate spatial conversions allows rapid and error-free sharing of locations. Google Maps URLs allow rapid navigation to RVs and an accurate assessment of ETA.



### Methodology

<img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/OperationalOverview.png" height="300">

*Data collection (red), augmentation (green) and serving (blue) are the responsibility of the team data controller*
  
- **Data Collection** - download and open [```Mapping.qgz```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/Mapping.qgz), a [QGIS](https://qgis.org/en/site/) project containing various web map services for remote location mapping. Generate WGS84 longitude, latitude coordinates for each location and paste them into a spreadsheet template ([```APs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/APs_Master.ods) or [```RVs_Master.ods```](https://github.com/EdwardALockhart/SpatialDataIncidentResponse/raw/main/RVs_Master.ods)) depending on the location type, adding additional information and columns as required (these will be unaltered and will carry through)

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Coordinates.png" height="300">
  
  *Extracting longitude, latitude coordinates for a location using right-click with the hand tool selected in QGIS*

- **Data Augmentation** - visit [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) and follow the instructions to automatically add spatial conversions and metadata to the spreadsheet records which are exported in a variety of formats (.csv, .gpkg, .gpx) for serving

- **Data Serving** - serve the exported files according to your requirements, free and open source examples are shown below

  - **Google Maps** (reads files from Google Drive; private online access)

      <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Google.png" height="300">


  - **QGIS** (can ingest any spatial data format; local PC only)

    <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/QGIS.png" height="300">


  - **Mobile / GPS Device** (uses .gpx files for import; offline navigation and data access)

    <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Mobile.png" height="300">

### [```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb)
[```AugmentLocations.ipynb```](https://colab.research.google.com/github/EdwardALockhart/SpatialDataIncidentResponse/blob/main/AugmentLocations.ipynb) is created for use with [Google Colaboratory](https://colab.research.google.com/), where python code can be run temporarily in the cloud, so no setup is required on your local PC. It runs in a web browser and accesses files hosted on your Google Drive for persistent storage between sessions, and therefore requires a free Google account. The code can also be used on a local PC with a python installation, [Anaconda](https://www.anaconda.com/) is recommended.

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
    - MobileCoverage - Minimum outdoor mobile phone coverage for all providers at buildings within a postcode

  <img src="https://github.com/EdwardALockhart/SpatialDataIncidentResponse/blob/main/Content/Augment.png" height="500">
  
  *How the original coordinates are converted and used to produce the spatial conversions and metadata*
  
- exports these data in a variety of formats (.csv, .gpkg, .gpx)
